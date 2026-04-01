# Assessment Sign-Off Backlog Tracker — How to Run

## What This Tool Does

This tool takes a CaseWorthy assessment export (Excel file) and generates a
formatted report showing how each office is performing on assessment sign-offs
month over month. It answers the question: is each office keeping up, falling
behind, or making progress on the backlog?

The output is an Excel workbook with three sheets:

1. **Summary** — The main tracker table. One row per office, with monthly columns
   showing new assessments, sign-offs, pending count, end-of-month backlog, and
   the change (delta) from the prior month. Green = improving, red = falling behind.
   Below the table is a legend explaining each column.

2. **Office Detail** — A simple summary per office: total assessments, current
   backlog, signed off count, pending review count, and % signed off.

3. **Raw Data** — The filtered and deduplicated dataset used to build the report.
   Useful for ad-hoc filtering or spot-checking.

---

## First-Time Setup (One Time Only)

You need Python installed on your computer. If you don't have it:
1. Download Python from https://www.python.org/downloads/
2. During install, **check the box** that says "Add Python to PATH"

Then open a terminal (PowerShell on Windows) and install the required packages:

```powershell
# Navigate to the project folder
cd "C:\Users\YourName\path\to\Month_Over_Month_Signoff_Report"

# Install dependencies (only need to do this once)
pip install -r assessment_tracker/requirements.txt
```

If you are using a virtual environment (.venv), activate it first:
```powershell
& ".venv\Scripts\Activate.ps1"
pip install -r assessment_tracker/requirements.txt
```

---

## Running the Report

### Step 1: Get the CaseWorthy Export
- Export the assessment data from CaseWorthy as an Excel file (.xlsx)
- Save it in the `assessment_tracker/input/` folder (optional — you can
  browse to any location, but the file picker opens to this folder by default)

### Step 2: Run the Script
Open PowerShell and run:

```powershell
cd "C:\Users\YourName\path\to\Month_Over_Month_Signoff_Report"
python assessment_tracker/main.py
```

Or if using a virtual environment:
```powershell
& ".venv\Scripts\python.exe" assessment_tracker/main.py
```

### Step 3: Select Your File
A file picker window will pop up. Select the CaseWorthy Excel export.

### Step 4: Review the Output
The script will:
- Process the data (you'll see progress in the terminal)
- Save the report to `assessment_tracker/output/`
- Automatically open the report in Excel

The output file is named `Assessment_SignOff_Tracker_YYYYMMDD.xlsx` with
today's date.

---

## Understanding the Output

### Summary Sheet Columns

| Column | What It Means |
|--------|---------------|
| **Baseline Backlog** | Assessments needing sign-off as of Aug 29, 2025 — the starting point |
| **New** | Assessments created that month (based on Begin Date) |
| **Signed Off** | Assessments approved that month (based on Assessment.LastModifiedDate) |
| **Pending** | Assessments sent back to the case manager — not approved, still in backlog |
| **End Backlog** | Total assessments still awaiting sign-off at month end |
| **Delta** | Change from prior month. Negative = improvement. Positive = falling behind |

### Colors
- **Green cells** = backlog decreased from the prior month (good)
- **Red cells** = backlog increased from the prior month (needs attention)
- Month headers alternate between dark and lighter blue to help visually
  separate the months

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "python is not recognized" | Python isn't in your PATH. Reinstall and check "Add to PATH" |
| "No module named pandas" | Run `pip install -r assessment_tracker/requirements.txt` |
| File picker doesn't appear | Make sure you're not running in a headless/remote terminal |
| Report shows unexpected numbers | Check that the export includes all required columns (see below) |

### Required Columns in the CaseWorthy Export
The export must include these columns (exact names):
- Client ID
- AssessmentID
- Program Name
- Type of Assessment
- Begin Date
- Assessment.LastModifiedDate
- Office Location
- Program Reviewed
- Program Review Status

---

## Notes

- The report **does not modify** your source file. It only reads from it.
- Each time you run, it generates a new dated output file (won't overwrite previous runs).
- Month ranges are detected automatically from the data — no need to update
  the code when new months appear.
- The Totals row uses Excel SUM formulas, so the sheet recalculates correctly.
