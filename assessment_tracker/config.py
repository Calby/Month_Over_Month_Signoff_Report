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

# Excel formatting
HEADER_DARK_BLUE = "1F4E79"
HEADER_MED_BLUE = "2E75B6"
HEADER_FONT_COLOR = "FFFFFF"
INCREASE_FILL = "FFCCCC"
DECREASE_FILL = "CCFFCC"
OFFICE_COL_WIDTH = 28
BASELINE_COL_WIDTH = 16
METRIC_COL_WIDTH = 12
