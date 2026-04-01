# Assessment Sign-Off Backlog Tracker — How to Run

## What This Tool Does

This tool takes a CaseWorthy assessment export (Excel file) and generates a
formatted report showing how each office is performing on assessment sign-offs
month over month. It answers the question: is each office keeping up, falling
behind, or making progress on the backlog?

The output is an Excel workbook with up to four sheets:

1. **Summary** — The main tracker table. One row per office, with monthly columns
   showing new assessments, sign-offs, pending count, end-of-month backlog, and
   the change (delta) from the prior month. Green = improving, red = falling behind.
   Below the table is a legend explaining each column.

2. **Office Detail** — A simple summary per office: total assessments, current
   backlog, signed off count, pending review count, and % signed off.

3. **Raw Data** — The filtered and deduplicated dataset used to build the report.
   Useful for ad-hoc filtering or spot-checking.

4. **Needs Attention** — Programs not in the mapping file. These records need
   either an office location added in CaseWorthy, or the program needs to be
   added to `program_mapping.xlsx`. This sheet only appears if there are
   unmapped programs.

---

## Option A: Running the .exe (Recommended)

No Python install needed. You should have a folder containing:

```
Assessment_Tracker/
    Assessment_Tracker.exe
    program_mapping.xlsx
    input/
    output/
```

### Steps:
1. Export the assessment data from CaseWorthy as an Excel file (.xlsx)
2. Save it in the `input/` folder (optional but convenient)
3. Double-click `Assessment_Tracker.exe`
4. A file picker will open — select your export file
5. The report will be saved in `output/` and open automatically in Excel

---

## Option B: Running from Python Source

### First-Time Setup (One Time Only)

You need Python installed on your computer. If you don't have it:
1. Download Python from https://www.python.org/downloads/
2. During install, **check the box** that says "Add Python to PATH"

Then open a terminal (PowerShell on Windows) and install the required packages:

```powershell
cd "C:\Users\YourName\path\to\Month_Over_Month_Signoff_Report"
pip install -r assessment_tracker/requirements.txt
```

If you are using a virtual environment (.venv), activate it first:
```powershell
& ".venv\Scripts\Activate.ps1"
pip install -r assessment_tracker/requirements.txt
```

### Running the Script

```powershell
cd "C:\Users\YourName\path\to\Month_Over_Month_Signoff_Report"
& ".venv\Scripts\python.exe" assessment_tracker/main.py
```

---

## Managing the Program Mapping

The file `program_mapping.xlsx` controls which programs are included in the
report and which office they belong to. It has two sheets:

### Mapping Sheet
| Program Name | Office Location |
|---|---|
| Tampa-VA Sup Services-P3-SSVF-Prevention 1010 | Tampa Office - SSVF |
| Polk-CoC-Returning Home 1050 | Lakeland Office |
| ... | ... |

**How it works:**
- If CaseWorthy already has an Office Location for the record, that is used
- If the Office Location is blank in CaseWorthy, the mapping provides the fallback
- If a program is NOT in this list (and not excluded), the record goes to the
  Needs Attention sheet

**To add a new program:** Open `program_mapping.xlsx`, go to the Mapping sheet,
and add a new row with the exact Program Name and the Office Location.

### Excluded Sheet
| Program Name |
|---|
| Charlotte-VA Supportive Services-SSVF-EHA |
| Bob Woodruff-All County-Assistance & SEHA 6004 |
| ... |

Programs on this sheet are completely removed from the report — they are not
tracked for sign-off.

**To exclude a program:** Add the exact Program Name to the Excluded sheet.

**Important:** Program names must match exactly (spelling, spacing, punctuation)
what appears in the CaseWorthy export. If you're unsure of the exact name,
check the Needs Attention sheet — it shows the program names as they appear
in the data.

---

## Understanding the Output

### Summary Sheet Columns

| Column | What It Means |
|--------|---------------|
| **Baseline Backlog** | Assessments needing sign-off as of Aug 29, 2025 — the starting point |
| **New** | Assessments created that month (based on Begin Date) |
| **Signed Off** | Assessments approved that month (based on Assessment.LastModifiedDate) |
| **Pending** | Assessments sent back to the case manager for review/changes — not approved, still in backlog |
| **End Backlog** | Total assessments still awaiting sign-off at month end |
| **Delta** | Change from prior month. Negative = improvement. Positive = falling behind |

### Colors
- **Green cells** = backlog decreased from the prior month (good)
- **Red cells** = backlog increased from the prior month (needs attention)
- Month headers alternate between dark and lighter blue to visually
  separate the months

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "program_mapping.xlsx not found" | Place it next to the .exe (or in the assessment_tracker folder if running from source) |
| All programs on Needs Attention | The mapping file is missing or empty — see above |
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

## Building the .exe (For Developers)

If you need to rebuild the .exe after code changes:

```powershell
pip install pyinstaller
python assessment_tracker/build_exe.py
```

The output goes to `assessment_tracker/dist/Assessment_Tracker/`. That entire
folder is what you distribute — it includes the .exe, the mapping file, and
the input/output folders.

---

## Notes

- The report **does not modify** your source file. It only reads from it.
- Each time you run, it generates a new dated output file (won't overwrite previous runs).
- Month ranges are detected automatically from the data — no need to update
  anything when new months appear.
- The Totals row uses Excel SUM formulas, so the sheet recalculates correctly.
