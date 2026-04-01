import os
import sys
import pandas as pd

BASELINE_DATE = "2025-08-29"
DEDUP_KEYS = [
    "Client ID",
    "AssessmentID",
    "Program Name",
    "Type of Assessment",
]
SIGNOFF_DATE_COL = "Assessment.LastModifiedDate"
BEGIN_DATE_COL = "Begin Date"
OFFICE_COL = "Office Location"
REVIEWED_COL = "Program Reviewed"
STATUS_COL = "Program Review Status"
APPROVED_STATUS = "Approved Eligibility Determination"
PENDING_STATUS_CONTAINS = "Pending"
OUTPUT_FILENAME = "Assessment_SignOff_Tracker.xlsx"
PROGRAM_COL = "Program Name"
MAPPING_FILENAME = "program_mapping.xlsx"

DATE_COLUMNS = [
    "Begin Date",
    "Assessment.LastModifiedDate",
    "Assessment.BeginAssessment",
    "Last Modified Date",
    "Last Case Note Date Per Prog",
]

# Columns to include in Raw Data sheet
RAW_DATA_COLUMNS = [
    "Client ID",
    "AssessmentID",
    "Program Name",
    "Type of Assessment",
    "Begin Date",
    "Assessment.LastModifiedDate",
    "Office Location",
    "Program Reviewed",
    "Program Review Status",
    "is_signed_off",
    "is_pending_review",
    "needs_signoff",
]

# Excel formatting
HEADER_DARK_BLUE = "1F4E79"
HEADER_MED_BLUE = "2E75B6"
HEADER_ALT_BLUE = "4472C4"
HEADER_ALT_MED = "5B9BD5"
HEADER_FONT_COLOR = "FFFFFF"
INCREASE_FILL = "FFCCCC"
DECREASE_FILL = "CCFFCC"
OFFICE_COL_WIDTH = 28
BASELINE_COL_WIDTH = 16
METRIC_COL_WIDTH = 12


def get_app_dir():
    """Return the application directory (works for both script and PyInstaller exe)."""
    if getattr(sys, "frozen", False):
        # Running as PyInstaller bundle — exe lives next to config files
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def load_program_mapping(mapping_path=None):
    """Load program-to-office mapping and exclusion list from Excel.

    Returns (program_to_office_dict, excluded_programs_list).
    """
    if mapping_path is None:
        mapping_path = os.path.join(get_app_dir(), MAPPING_FILENAME)

    if not os.path.exists(mapping_path):
        print(f"WARNING: Mapping file not found: {mapping_path}")
        print("  All programs will appear on the Needs Attention sheet.")
        return {}, []

    mapping_df = pd.read_excel(mapping_path, sheet_name="Mapping")
    program_to_office = dict(zip(
        mapping_df["Program Name"].astype(str).str.strip(),
        mapping_df["Office Location"].astype(str).str.strip(),
    ))

    try:
        excluded_df = pd.read_excel(mapping_path, sheet_name="Excluded")
        excluded = excluded_df["Program Name"].astype(str).str.strip().tolist()
    except Exception:
        excluded = []

    print(f"  Loaded mapping: {len(program_to_office)} programs, {len(excluded)} excluded")
    return program_to_office, excluded
