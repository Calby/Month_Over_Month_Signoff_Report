# Assessment Sign-Off Backlog Tracker — Handoff Document

**Prepared by:** James Calby, Data Systems Analyst
**Date:** April 2026
**For:** Whoever is taking over this report

---

## Quick Summary

This tool automates a monthly report that tracks whether each office is keeping
up with assessment sign-offs in CaseWorthy. You export the data from CaseWorthy,
run the tool, and it produces a formatted Excel report.

**You do not need to know Python or programming to use this tool.**

---

## What You'll Need

You should have a folder called `Assessment_Tracker` containing:

```
Assessment_Tracker/
    Assessment_Tracker.exe      ← the app (double-click to run)
    program_mapping.xlsx        ← controls which programs go to which office
    input/                      ← put your CaseWorthy exports here
    output/                     ← reports get saved here
```

If you're missing any of these files, contact your supervisor or IT.

---

## How to Run the Report (Step by Step)

### 1. Export Data from CaseWorthy
- Run your standard assessment export in CaseWorthy
- Save the file as an Excel file (.xlsx)
- Drop it in the `input/` folder (or anywhere you'll remember)

### 2. Open the App
- Double-click `Assessment_Tracker.exe`
- A window will open with the app

### 3. Select Your Files
- Click **Browse** next to "CaseWorthy Export File" and select your export
- The Output Folder defaults to the `output/` folder — you can change it if
  you want the report saved somewhere else

### 4. Generate the Report
- Click the **Generate Report** button
- The progress bar will animate while it processes
- When it finishes, it will ask if you want to open the report — click Yes

### 5. Review the Report
- The report is an Excel file named `Assessment_SignOff_Tracker_YYYYMMDD.xlsx`
- It won't overwrite previous reports — each run creates a new dated file

---

## Understanding the Report

### Summary Sheet (the main one)

This is the sheet you'll share with leadership. It shows one row per office,
with monthly columns tracking the backlog.

| Column | What It Means |
|--------|---------------|
| **Baseline Backlog** | How many assessments were waiting for sign-off on August 29, 2025 — the starting point |
| **New** | How many new assessments came in that month |
| **Signed Off** | How many assessments were approved that month |
| **Pending** | Assessments sent back to the case manager for changes — NOT approved, still in the backlog |
| **End Backlog** | Total assessments still waiting for sign-off at the end of that month |
| **Delta** | The change from the previous month. Negative = getting better. Positive = falling behind |

**Colors:**
- **Green** = backlog went down (good)
- **Red** = backlog went up (needs attention)
- Month headers alternate between dark and light blue so you can tell months apart

### Office Detail Sheet

A simple snapshot of each office: total assessments, current backlog, how many
are signed off, how many are pending, and the % signed off. Sorted by highest
backlog first.

### Raw Data Sheet

The cleaned-up dataset the report is built from. Only the columns that matter
are included. Useful if someone asks "where did that number come from?" — you
can filter and check.

### Needs Attention Sheet

**This is the one that might require action from you.**

If a program name from CaseWorthy doesn't match anything in the mapping file,
the record lands here. This means either:
1. Someone needs to add the Office Location in CaseWorthy for that client, OR
2. You need to add the program to `program_mapping.xlsx` (see below)

If this sheet is empty or doesn't appear, everything mapped correctly.

---

## Managing the Program Mapping

The file `program_mapping.xlsx` sits next to the .exe. It's a regular Excel
file with two sheets. **You will need to update this occasionally** when new
programs are added in CaseWorthy.

### Mapping Sheet — "This program belongs to this office"

Two columns: **Program Name** and **Office Location**.

| Program Name | Office Location |
|---|---|
| Tampa-VA Sup Services-P3-SSVF-Prevention 1010 | Tampa Office - SSVF |
| Polk-CoC-Returning Home 1050 | Lakeland Office |

**How the app uses this:**
1. First, it checks if CaseWorthy already has an office for the record
2. If CaseWorthy's office is blank, it uses this mapping as a fallback
3. If the program isn't in this list at all, it goes to the Needs Attention sheet

**To add a new program:**
1. Open `program_mapping.xlsx`
2. Go to the **Mapping** sheet
3. Add a new row at the bottom
4. Type the **exact** Program Name as it appears in CaseWorthy (spelling,
   spacing, dashes — it has to match perfectly)
5. Type the Office Location
6. Save and close the file
7. Re-run the report

**Tip:** If you're not sure of the exact program name, check the Needs Attention
sheet — it shows the name exactly as CaseWorthy has it. Copy and paste it.

### Excluded Sheet — "Ignore these programs"

One column: **Program Name**. These programs are completely removed from the
report. Currently this includes all SSVF-EHA programs and the Bob Woodruff
program.

**To exclude a new program:**
1. Open `program_mapping.xlsx`
2. Go to the **Excluded** sheet
3. Add the exact Program Name
4. Save and close

---

## Common Scenarios

### "A new program was added in CaseWorthy"
1. Run the report — the program will show up on the Needs Attention sheet
2. Copy the exact program name from that sheet
3. Open `program_mapping.xlsx` → Mapping sheet
4. Paste the program name, add the office location
5. Save, re-run the report

### "The report shows an office I don't recognize"
The office name comes from CaseWorthy first, then the mapping file. Check if
someone entered a non-standard office name in CaseWorthy and either fix it
there or add the variant to the mapping.

### "The numbers look wrong for an office"
Check the Raw Data sheet — filter by that office and compare. Most likely a
program is mapped to the wrong office in `program_mapping.xlsx`, or records
in CaseWorthy have an incorrect office. Fix the mapping or the CaseWorthy
data and re-run.

### "I need to change the baseline date"
This requires a code change. Contact whoever manages the Python source code.
The baseline is set in `config.py` as `BASELINE_DATE = "2025-08-29"`.

### "The .exe won't open / Windows blocks it"
Windows SmartScreen may block it since it's not a signed application.
Click "More info" → "Run anyway". If your organization blocks unsigned
executables, you'll need to run from Python source instead (see the
HOW_TO_RUN.md file for instructions).

---

## What NOT to Do

- **Don't rename `program_mapping.xlsx`** — the app looks for this exact filename
- **Don't move the .exe out of its folder** — it needs the mapping file and
  input/output folders next to it
- **Don't modify the CaseWorthy export before running** — the app expects the
  raw export; it handles all the cleanup
- **Don't delete old reports from output/** — they don't take up much space
  and you might need to compare months

---

## Files at a Glance

| File | What It Is | Do You Edit It? |
|------|-----------|-----------------|
| `Assessment_Tracker.exe` | The app | No — just double-click to run |
| `program_mapping.xlsx` | Program → Office mapping + exclusions | **Yes** — when new programs appear |
| `input/` | Where you put CaseWorthy exports | Drop files here |
| `output/` | Where reports are saved | Reports appear here automatically |

---

## Getting Help

- Check `HOW_TO_RUN.md` for detailed technical instructions
- For code changes or rebuilding the .exe, contact your Data Systems team
- The source code is in the GitHub repository under `assessment_tracker/`
