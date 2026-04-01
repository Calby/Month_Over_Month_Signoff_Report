"""Validate processor dedup, classification, and backlog logic with synthetic data."""
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, ".")
from processor import deduplicate, classify, exclude_programs, apply_program_office_mapping, _backlog_at_date, build_monthly_table
from config import DEDUP_KEYS, SIGNOFF_DATE_COL, BEGIN_DATE_COL, OFFICE_COL, REVIEWED_COL, STATUS_COL, PROGRAM_COL


def make_row(client_id, assess_id, program, assess_type, begin, modified,
             office, reviewed, status):
    return {
        "Client ID": client_id,
        "AssessmentID": assess_id,
        "Program Name": program,
        "Type of Assessment": assess_type,
        BEGIN_DATE_COL: pd.Timestamp(begin),
        SIGNOFF_DATE_COL: pd.Timestamp(modified) if modified else pd.NaT,
        OFFICE_COL: office,
        REVIEWED_COL: reviewed,
        STATUS_COL: status,
    }


def test_dedup():
    """Test exact-dup removal and key-based dedup keeping most recent."""
    rows = [
        # Exact duplicate pair
        make_row(1, 100, "ProgA", "Program Enrollment", "2025-09-01", "2025-09-15", "Office1", "Yes", "Approved Eligibility Determination"),
        make_row(1, 100, "ProgA", "Program Enrollment", "2025-09-01", "2025-09-15", "Office1", "Yes", "Approved Eligibility Determination"),
        # Same key, different modified dates — should keep the newer one
        make_row(2, 200, "ProgB", "Program Exit", "2025-09-05", "2025-10-01", "Office2", "No", ""),
        make_row(2, 200, "ProgB", "Program Exit", "2025-09-05", "2025-09-10", "Office2", "Yes", "Approved Eligibility Determination"),
        # Unique row
        make_row(3, 300, "ProgC", "90 Day/Annual Recert or Update", "2025-10-01", "2025-10-20", "Office1", "Yes", "Pending Approval"),
    ]
    df = pd.DataFrame(rows)
    assert len(df) == 5, f"Expected 5 raw rows, got {len(df)}"

    result = deduplicate(df)
    assert len(result) == 3, f"Expected 3 after dedup, got {len(result)}"

    # The kept row for client 2 should be the newer one (Oct 1)
    row_c2 = result[result["Client ID"] == 2].iloc[0]
    assert row_c2[SIGNOFF_DATE_COL] == pd.Timestamp("2025-10-01"), "Should keep most recent"
    assert row_c2[REVIEWED_COL] == "No", "Most recent row for client 2 has Reviewed=No"
    print("  PASS: dedup")


def test_classify():
    """Test classification logic for signed off, pending, needs signoff."""
    rows = [
        make_row(1, 100, "P", "T", "2025-09-01", "2025-09-15", "O1", "Yes", "Approved Eligibility Determination"),
        make_row(2, 200, "P", "T", "2025-09-01", "2025-09-15", "O1", "Yes", "Pending Approval"),
        make_row(3, 300, "P", "T", "2025-09-01", "2025-09-15", "O1", "No", ""),
        make_row(4, 400, "P", "T", "2025-09-01", None, "O1", "No", np.nan),
    ]
    df = pd.DataFrame(rows)
    df = classify(df)

    # Row 0: signed off
    assert df.loc[0, "is_signed_off"] == True
    assert df.loc[0, "is_pending_review"] == False
    assert df.loc[0, "needs_signoff"] == False

    # Row 1: pending — NOT signed off
    assert df.loc[1, "is_signed_off"] == False
    assert df.loc[1, "is_pending_review"] == True
    assert df.loc[1, "needs_signoff"] == True

    # Row 2: not reviewed
    assert df.loc[2, "is_signed_off"] == False
    assert df.loc[2, "is_pending_review"] == False
    assert df.loc[2, "needs_signoff"] == True

    # Row 3: NaN status, not reviewed
    assert df.loc[3, "is_signed_off"] == False
    assert df.loc[3, "is_pending_review"] == False
    assert df.loc[3, "needs_signoff"] == True

    print("  PASS: classify")


def test_backlog_at_date():
    """Test point-in-time backlog reconstruction."""
    rows = [
        # Began before baseline, still needs signoff → in baseline backlog
        make_row(1, 100, "P", "T", "2025-08-01", None, "O1", "No", ""),
        # Began before baseline, signed off AFTER baseline → in baseline backlog
        make_row(2, 200, "P", "T", "2025-08-15", "2025-09-10", "O1", "Yes", "Approved Eligibility Determination"),
        # Began before baseline, signed off BEFORE baseline → NOT in backlog
        make_row(3, 300, "P", "T", "2025-07-01", "2025-08-20", "O1", "Yes", "Approved Eligibility Determination"),
        # Began AFTER baseline → NOT in baseline backlog
        make_row(4, 400, "P", "T", "2025-09-05", None, "O1", "No", ""),
    ]
    df = pd.DataFrame(rows)
    df = classify(df)
    df[OFFICE_COL] = df[OFFICE_COL].fillna("Unassigned")

    baseline = pd.Timestamp("2025-08-29")
    backlog = _backlog_at_date(df, baseline)

    assert backlog.get("O1", 0) == 2, f"Expected 2 in backlog at baseline, got {backlog.get('O1', 0)}"

    # At Sep 30: record 2 signed off Sep 10, so no longer in backlog. Record 4 now in backlog.
    sep30 = pd.Timestamp("2025-09-30")
    backlog_sep = _backlog_at_date(df, sep30)
    # Record 1: began Aug 1, needs signoff → yes
    # Record 2: signed off Sep 10 ≤ Sep 30 → not in backlog
    # Record 3: signed off Aug 20 ≤ Sep 30 → not in backlog
    # Record 4: began Sep 5 ≤ Sep 30, needs signoff → yes
    assert backlog_sep.get("O1", 0) == 2, f"Expected 2 at Sep 30, got {backlog_sep.get('O1', 0)}"

    print("  PASS: backlog_at_date")


def test_monthly_table():
    """Test full monthly table build with a small dataset."""
    rows = [
        # Office A: 2 in baseline backlog, 1 new in Sep, 1 signed off in Sep
        make_row(1, 100, "P", "T", "2025-08-01", None, "OfficeA", "No", ""),
        make_row(2, 200, "P", "T", "2025-08-15", "2025-09-15", "OfficeA", "Yes", "Approved Eligibility Determination"),
        make_row(3, 300, "P", "T", "2025-09-10", "2025-09-20", "OfficeA", "Yes", "Approved Eligibility Determination"),
        # Office B: 1 in baseline, pending
        make_row(4, 400, "P", "T", "2025-08-20", "2025-09-05", "OfficeB", "Yes", "Pending Approval"),
        # Unassigned office
        make_row(5, 500, "P", "T", "2025-09-01", None, np.nan, "No", ""),
    ]
    df = pd.DataFrame(rows)
    from processor import deduplicate as dd
    df = dd(df)
    df = classify(df)
    df[OFFICE_COL] = df[OFFICE_COL].fillna("Unassigned")
    result = build_monthly_table(df)

    assert "OfficeA" in result["offices"]
    assert "OfficeB" in result["offices"]
    assert "Unassigned" in result["offices"]

    # Baseline: OfficeA=2 (records 1 needs signoff, record 2 signed off after baseline)
    assert result["baseline"]["OfficeA"] == 2, f"OfficeA baseline: {result['baseline']['OfficeA']}"
    # OfficeB=1 (record 4 pending = needs signoff)
    assert result["baseline"]["OfficeB"] == 1, f"OfficeB baseline: {result['baseline']['OfficeB']}"

    # Sep data
    sep = result["monthly_data"][(2025, 9)]
    # New in Sep: record 3 (OfficeA), record 5 (Unassigned)
    assert sep["new"]["OfficeA"] == 1
    assert sep["new"]["Unassigned"] == 1
    # Signed off in Sep: record 2 and 3 (OfficeA)
    assert sep["signed_off"]["OfficeA"] == 2
    # EOM backlog OfficeA at Sep 30: record 1 (needs signoff, began before Sep 30) = 1
    assert sep["eom_backlog"]["OfficeA"] == 1, f"OfficeA Sep EOM: {sep['eom_backlog']['OfficeA']}"

    print("  PASS: monthly_table")


def test_exclude_programs():
    """Excluded programs should be removed from the dataset."""
    rows = [
        make_row(1, 100, "Charlotte-VA Supportive Services-SSVF-EHA", "T", "2025-09-01", None, "O1", "No", ""),
        make_row(2, 200, "Tampa-VA Sup Services-P3-SSVF-Prevention 1010", "T", "2025-09-01", None, "O1", "No", ""),
        make_row(3, 300, "Bob Woodruff-All County-Assistance & SEHA 6004", "T", "2025-09-01", None, "O1", "No", ""),
    ]
    df = pd.DataFrame(rows)
    excluded_list = [
        "Charlotte-VA Supportive Services-SSVF-EHA",
        "Bob Woodruff-All County-Assistance & SEHA 6004",
    ]
    kept, excluded = exclude_programs(df, excluded_list)
    assert len(excluded) == 2, f"Expected 2 excluded, got {len(excluded)}"
    assert len(kept) == 1, f"Expected 1 kept, got {len(kept)}"
    assert kept.iloc[0]["Client ID"] == 2
    print("  PASS: exclude_programs")


def test_program_office_mapping():
    """CaseWorthy office takes priority; mapping is fallback for missing offices."""
    rows = [
        # Known program WITH CaseWorthy office — should KEEP CaseWorthy office
        make_row(1, 100, "Tampa-VA Sup Services-P3-SSVF-Prevention 1010", "T", "2025-09-01", None, "Some CW Office", "No", ""),
        # Known program with NaN office — should fall back to mapping
        make_row(2, 200, "Polk-CoC-Returning Home 1050", "T", "2025-09-01", None, np.nan, "No", ""),
        # Known program with empty string office — should fall back to mapping
        make_row(3, 300, "Sarasota-CoC-Returning Home 1051", "T", "2025-09-01", None, "", "No", ""),
        # Unknown program — should go to unmapped
        make_row(4, 400, "Some Unknown Program", "T", "2025-09-01", None, "O1", "No", ""),
    ]
    df = pd.DataFrame(rows)
    test_mapping = {
        "Tampa-VA Sup Services-P3-SSVF-Prevention 1010": "Tampa Office - SSVF",
        "Polk-CoC-Returning Home 1050": "Lakeland Office",
        "Sarasota-CoC-Returning Home 1051": "Sarasota Office",
    }
    mapped, unmapped = apply_program_office_mapping(df, test_mapping)

    assert len(mapped) == 3
    assert len(unmapped) == 1
    # CaseWorthy office preserved when present
    assert mapped.iloc[0][OFFICE_COL] == "Some CW Office", f"Expected CW office, got {mapped.iloc[0][OFFICE_COL]}"
    # Mapping used as fallback when office is missing
    assert mapped.iloc[1][OFFICE_COL] == "Lakeland Office", f"Expected fallback, got {mapped.iloc[1][OFFICE_COL]}"
    assert mapped.iloc[2][OFFICE_COL] == "Sarasota Office", f"Expected fallback, got {mapped.iloc[2][OFFICE_COL]}"
    # Unknown goes to unmapped
    assert unmapped.iloc[0][PROGRAM_COL] == "Some Unknown Program"
    print("  PASS: program_office_mapping")


if __name__ == "__main__":
    print("Running processor tests...")
    test_dedup()
    test_classify()
    test_backlog_at_date()
    test_monthly_table()
    test_exclude_programs()
    test_program_office_mapping()
    print("\nAll tests passed!")
