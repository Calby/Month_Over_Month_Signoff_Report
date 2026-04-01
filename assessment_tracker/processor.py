import pandas as pd
import numpy as np
from config import (
    BASELINE_DATE, DEDUP_KEYS, SIGNOFF_DATE_COL, BEGIN_DATE_COL,
    OFFICE_COL, REVIEWED_COL, STATUS_COL, APPROVED_STATUS,
    PENDING_STATUS_CONTAINS, DATE_COLUMNS, PROGRAM_COL,
    EXCLUDED_PROGRAMS, PROGRAM_TO_OFFICE,
)


def load_data(filepath: str) -> pd.DataFrame:
    """Load Excel export and parse date columns."""
    df = pd.read_excel(filepath)
    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Two-pass dedup: exact duplicates, then keep most recent per key combo."""
    df = df.drop_duplicates()
    df = df.sort_values(SIGNOFF_DATE_COL, ascending=False, na_position="last")
    df = df.drop_duplicates(subset=DEDUP_KEYS, keep="first")
    return df.reset_index(drop=True)


def classify(df: pd.DataFrame) -> pd.DataFrame:
    """Add classification boolean columns."""
    df["is_signed_off"] = (
        (df[REVIEWED_COL].astype(str).str.strip() == "Yes")
        & (df[STATUS_COL].astype(str).str.strip() == APPROVED_STATUS)
    )
    df["is_pending_review"] = (
        (df[REVIEWED_COL].astype(str).str.strip() == "Yes")
        & (df[STATUS_COL].astype(str).str.contains(PENDING_STATUS_CONTAINS, case=False, na=False))
    )
    df["needs_signoff"] = ~df["is_signed_off"]
    return df


def exclude_programs(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Remove excluded programs. Returns (kept, excluded)."""
    mask = df[PROGRAM_COL].isin(EXCLUDED_PROGRAMS)
    return df[~mask].reset_index(drop=True), df[mask].reset_index(drop=True)


def apply_program_office_mapping(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Map program names to offices. Returns (mapped_df, unmapped_df).

    Records whose program is in PROGRAM_TO_OFFICE get that office assigned
    (overriding whatever CaseWorthy had). Records whose program is NOT in the
    mapping are separated out as 'needs attention' for manual review.
    """
    known = df[PROGRAM_COL].isin(PROGRAM_TO_OFFICE)
    mapped_df = df[known].copy()
    unmapped_df = df[~known].copy()

    # Override office from the mapping
    mapped_df[OFFICE_COL] = mapped_df[PROGRAM_COL].map(PROGRAM_TO_OFFICE)

    return mapped_df.reset_index(drop=True), unmapped_df.reset_index(drop=True)


def _backlog_at_date(df: pd.DataFrame, d: pd.Timestamp) -> pd.Series:
    """Count backlog per office at a point in time.

    A record is in backlog at date D if:
    - Begin Date <= D
    - AND (needs_signoff == True OR (is_signed_off AND signoff_date > D))
    """
    began = df[BEGIN_DATE_COL] <= d
    still_needs = df["needs_signoff"]
    signed_off_later = df["is_signed_off"] & (df[SIGNOFF_DATE_COL] > d)
    in_backlog = began & (still_needs | signed_off_later)
    return df.loc[in_backlog].groupby(OFFICE_COL).size()


def build_monthly_table(df: pd.DataFrame) -> dict:
    """Build the full monthly backlog table.

    Returns a dict with:
        - offices: sorted list of office names
        - baseline: Series of baseline backlog per office
        - months: list of (year, month) tuples in order
        - monthly_data: dict keyed by (year, month) with per-office metrics
        - detail: DataFrame for Sheet 4 office detail
        - raw: the classified DataFrame
    """
    baseline_dt = pd.Timestamp(BASELINE_DATE)

    # Determine month range from data
    all_dates = pd.concat([
        df[BEGIN_DATE_COL].dropna(),
        df[SIGNOFF_DATE_COL].dropna(),
    ])
    min_date = all_dates.min()
    max_date = all_dates.max()

    # Build list of months from baseline month+1 through last month with data
    start_period = baseline_dt.to_period("M") + 1  # Sep 2025
    end_period = max_date.to_period("M")
    months = []
    p = start_period
    while p <= end_period:
        months.append((p.year, p.month))
        p += 1

    # All offices sorted
    offices = sorted(df[OFFICE_COL].unique(), key=lambda x: (x == "Unassigned", x))

    # Baseline backlog
    baseline = _backlog_at_date(df, baseline_dt).reindex(offices, fill_value=0)

    # Monthly metrics
    monthly_data = {}
    for year, month in months:
        month_start = pd.Timestamp(year=year, month=month, day=1)
        month_end = month_start + pd.offsets.MonthEnd(0)

        in_month_begin = (df[BEGIN_DATE_COL].dt.year == year) & (df[BEGIN_DATE_COL].dt.month == month)
        in_month_signoff = (
            df["is_signed_off"]
            & (df[SIGNOFF_DATE_COL].dt.year == year)
            & (df[SIGNOFF_DATE_COL].dt.month == month)
        )
        pending_in_month = (
            df["is_pending_review"]
            & (df[BEGIN_DATE_COL].dt.year == year)
            & (df[BEGIN_DATE_COL].dt.month == month)
        )

        new_by_office = df.loc[in_month_begin].groupby(OFFICE_COL).size().reindex(offices, fill_value=0)
        signed_by_office = df.loc[in_month_signoff].groupby(OFFICE_COL).size().reindex(offices, fill_value=0)
        pending_by_office = df.loc[pending_in_month].groupby(OFFICE_COL).size().reindex(offices, fill_value=0)
        eom_backlog = _backlog_at_date(df, month_end).reindex(offices, fill_value=0)

        monthly_data[(year, month)] = {
            "new": new_by_office,
            "signed_off": signed_by_office,
            "pending": pending_by_office,
            "eom_backlog": eom_backlog,
        }

    # Office detail for Sheet 4
    detail = df.groupby(OFFICE_COL).agg(
        total_assessments=("is_signed_off", "count"),
        signed_off_count=("is_signed_off", "sum"),
        pending_review_count=("is_pending_review", "sum"),
        needs_signoff_count=("needs_signoff", "sum"),
    ).reindex(offices)
    # Current backlog = needs_signoff count
    detail["current_backlog"] = detail["needs_signoff_count"]
    detail["pct_signed_off"] = (detail["signed_off_count"] / detail["total_assessments"] * 100).round(1)
    detail = detail.sort_values("current_backlog", ascending=False)

    return {
        "offices": offices,
        "baseline": baseline,
        "months": months,
        "monthly_data": monthly_data,
        "detail": detail,
        "raw": df,
    }


def process_data(filepath: str) -> dict:
    """Full pipeline: load → dedup → exclude → map offices → classify → build."""
    df = load_data(filepath)
    print(f"  Loaded: {len(df):,} rows")
    df = deduplicate(df)
    print(f"  After dedup: {len(df):,} rows")

    # Exclude programs not tracked for sign-off
    df, excluded = exclude_programs(df)
    print(f"  Excluded programs: {len(excluded):,} rows")

    # Apply program → office mapping; separate unmapped records
    df, unmapped = apply_program_office_mapping(df)
    print(f"  Mapped to offices: {len(df):,} rows")
    print(f"  Unmapped (needs attention): {len(unmapped):,} rows")

    df = classify(df)
    # Classify unmapped too so the Needs Attention sheet has those columns
    if len(unmapped) > 0:
        unmapped = classify(unmapped)
        unmapped[OFFICE_COL] = unmapped[OFFICE_COL].fillna("Unassigned")

    print(f"  Offices: {df[OFFICE_COL].nunique()}")
    print(f"  Signed off: {df['is_signed_off'].sum():,}")
    print(f"  Pending review: {df['is_pending_review'].sum():,}")
    print(f"  Needs sign-off: {df['needs_signoff'].sum():,}")
    result = build_monthly_table(df)
    result["unmapped"] = unmapped
    print(f"  Baseline backlog (Aug 29): {result['baseline'].sum():,}")
    print(f"  Months in data: {len(result['months'])}")
    return result
