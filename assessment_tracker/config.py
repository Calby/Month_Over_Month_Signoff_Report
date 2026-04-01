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

# Programs excluded from the report entirely (not tracked for sign-off)
EXCLUDED_PROGRAMS = [
    "Charlotte-VA Supportive Services-SSVF-EHA",
    "MidFlorida-VA Supportive Services-SSVF-EHA",
    "Orlando-VA Supportive Services-SSVF-EHA",
    "Pasco-VA Supportive Services-SSVF-EHA",
    "Pinellas-VA Supportive Services-SSVF-EHA",
    "Polk-VA Supportive Services-SSVF-EHA",
    "Sarasota-VA Supportive Services-SSVF-EHA",
    "Sebring-VA Supportive Services-SSVF-EHA",
    "SouthWest-VA Supportive Services-SSVF-EHA",
    "Tampa-VA Supportive Services-SSVF-EHA",
    "San Juan-VA Supportive Services-SSVF-EHA",
    "Bob Woodruff-All County-Assistance & SEHA 6004",
]

# Program → Office mapping (overrides CaseWorthy Office Location)
PROGRAM_TO_OFFICE = {
    "All-County-VA-Suicide-Prevention 1114": "SSG Fox",

    "Charlotte CARE Center ESG/Challenge-RRH": "Port Charlotte Office",
    "Charlotte County-SHIP-RRH 1305": "Port Charlotte Office",
    "Charlotte-Care Center-Family Shelter": "Port Charlotte Care Center Shelter",
    "Charlotte-Care Center-HCHV-VA Shelter-TH 1215": "Port Charlotte Care Center Shelter",
    "Charlotte-Care Center-Individual Shelter": "Port Charlotte Care Center Shelter",
    "Charlotte-Challenge RRH 1200": "Port Charlotte Office",
    "Charlotte-DEO-Recovery Grant-RRH 1216": "Port Charlotte Office",
    "Charlotte-SW-HUD-CoC-DV RRH 1123": "Port Charlotte Office",
    "Charlotte-VA Sup Services-SSVF-Prevention 1010": "Port Charlotte Office",
    "Charlotte-VA Supportive Services-SSVF-RRH 1010": "Port Charlotte Office",

    "Citrus Mid FL-HUD-CoC-RRH 1142": "Citrus Office",
    "Lake Mid FL-HUD-CoC-RRH 1142": "Citrus Office",
    "MidFlorida-HUD-CoC-Consolidated-RRH 1175": "Citrus Office",
    "MidFlorida-VA Sup Services-SSVF-Prevention 1010": "Citrus Office",
    "MidFlorida-VA Supportive Services-SSVF-RRH 1010": "Citrus Office",

    "Orlando-Seminole-County-HOME ARP-RRH 1315": "Orlando Office",
    "Orlando-VA Sup Services-SSVF-Prevention 1010": "Orlando Office",
    "Orlando-VA Supportive Services-SSVF-RRH 1010": "Orlando Office",

    "Pasco-HUD-CoC-Bonus RRH 1120": "New Port Richey Office",
    "Pasco-HUD-CoC-Consolidated RRH 1122": "New Port Richey Office",
    "Pasco-HUD-CoC-DV RRH 1121": "New Port Richey Office",
    "Pasco-VA Sup Services-Renew-SSVF-Prevention 1010": "New Port Richey Office",
    "Pasco-VA Supportive Services-Renew-SSVF-RRH 1010": "New Port Richey Office",

    "Pasco-Various-Ozanam-III-PSH 1101": "Pasco - PSH",
    "Pasco-Various-Ozanam-II-PSH 1100": "Pasco - PSH",
    "Pasco-Various-Ozanam-I-PSH 1021": "Pasco - PSH",
    "Pasco-Various-RosalieRendu-PSH 1021": "Pasco - PSH",
    "Sarasota-Heroes-Village-PSH 7201": "Sarasota - PSH",

    "Pinellas PCF Rapid Resolution for Seniors 1227": "Pinellas Care Center Shelter",
    "Pinellas-Care Center-Night Shelter-ES 1008": "Pinellas Care Center Shelter",
    "Pinellas-COH-Bridging Families Shelter-ES 1235": "Pinellas Center of Hope Office",
    "Pinellas-COH-Family Shelter-JWB-ES 1080": "Pinellas Center of Hope Office",
    "Pinellas-Family Hotel/Motels-JWB-SEHA 1080": "Pinellas Care Center Shelter",
    "Pinellas-HLA-Challenge-Rapid Resolution 1225": "Pinellas Care Center Shelter",

    "Pinellas-COH-VA 20 Bed HCHV-TH 1005": "Pinellas Center of Hope Office",
    "Pinellas-COH-VA Bridge Housing-TH 1001": "Pinellas Center of Hope Office",
    "Pinellas-COH-VA Low Demand-ES 1001": "Pinellas Center of Hope Office",

    "Pinellas-VA Sup Services-P2-SSVF-Prevention 1010": "Clearwater Office SSVF",
    "Pinellas-VA Supportive Services-P2-SSVF-RRH 1010": "Clearwater Office SSVF",

    "Pinellas-City of St.Pete-SAF-Rapid Resolution 1332": "Clearwater Office - Non Veteran",
    "Pinellas-Collab-Rapid Rehousing-RRH 1023": "Clearwater Office - Non Veteran",
    "Pinellas-Families-JWB-RRH 1080": "Clearwater Office - Non Veteran",

    "Polk-Coalition-ESG RUSH RRH 1133": "Lakeland Office",
    "Polk-Coalition-LPO42-ESG-RRH 1013": "Lakeland Office",
    "Polk-CoC-Returning Home 1050": "Lakeland Office",
    "Polk-County-ESG RUSH RRH 1230": "Lakeland Office",
    "Polk-VA Sup Services-P5-SSVF-Prevention 1010": "Lakeland Office",
    "Polk-VA Supportive Services-P5-SSVF-RRH 1010": "Lakeland Office",

    "Sarasota & Manatee-Suncoast-ESG-RRH 1025": "Sarasota Office",
    "Sarasota-CoC-Returning Home 1051": "Sarasota Office",
    "Sarasota-County-HSAC SEHA 1185": "Sarasota Office",
    "Sarasota-County-HSAC-RRH Essentials 1250": "Sarasota Office",
    "Sarasota-VA Sup Services-SSVF-Prevention 1010": "Sarasota Office",
    "Sarasota-VA Supportive Services-SSVF-RRH 1010": "Sarasota Office",

    "Sebring-VA Sup Services-SSVF-Prevention 1010": "Sebring Office",
    "Sebring-VA Supportive Services-SSVF-RRH 1010": "Sebring Office",

    "SouthWest-VA Sup Services-SSVF-Prevention 1010": "Fort Myers Office",
    "SouthWest-VA Supportive Services-SSVF-RRH 1010": "Fort Myers Office",

    "Tampa-Hillsborough-County-RUSH RRH 1326": "Tampa Office - Non Veteran",
    "Tampa-THHI-ESG DAP CES 1107": "Tampa Office - Non Veteran",
    "Tampa-THHI-State-ESG RUSH RRH 1325": "Tampa Office - Non Veteran",
    "Tampa-THHI-State-ESG-RUSH SEHA 1325": "Tampa Office - Non Veteran",

    "Tampa-VA Sup Services-P3-SSVF-Prevention 1010": "Tampa Office - SSVF",
    "Tampa-VA Supportive Services-P3-SSVF-RRH 1010": "Tampa Office - SSVF",

    "Pre-Housing Bay Pines-VA-GPD-Case Mgmt 1034": "GPD South",
    "Pre-Housing James Haley-VA-GPD-Case Mgmt 1141": "GPD South",
    "Retention Bay Pines-VA-GPD-Case Mgmt 1034": "GPD North",
    "Retention James Haley-VA-GPD-Case Mgmt 1141": "GPD North",
}

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
