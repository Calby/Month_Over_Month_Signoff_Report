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
HEADER_ALT_BLUE = "4472C4"       # Alternating month color (lighter)
HEADER_ALT_MED = "5B9BD5"        # Alternating sub-header color
HEADER_FONT_COLOR = "FFFFFF"
INCREASE_FILL = "FFCCCC"
DECREASE_FILL = "CCFFCC"
OFFICE_COL_WIDTH = 28
BASELINE_COL_WIDTH = 16
METRIC_COL_WIDTH = 12
