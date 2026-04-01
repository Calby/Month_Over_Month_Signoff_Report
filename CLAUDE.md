# CLAUDE.md - Project Changelog & Notes

## Project: Month Over Month Signoff Report

## Architecture Overview

This app takes a CaseWorthy assessment Excel export and produces a formatted
Excel workbook showing office-by-office sign-off backlog trends from
August 29, 2025 forward.

### File Structure
```
assessment_tracker/
├── main.py              # Entry point — file picker, runs pipeline, opens output
├── processor.py         # Data logic: load, dedup, classify, monthly backlog calc
├── report_builder.py    # Excel output: Summary, Office Detail, Raw Data sheets
├── config.py              # Constants, path helpers, mapping loader
├── program_mapping.xlsx   # Editable: program→office mapping + exclusion list
├── build_exe.py           # PyInstaller build script to create .exe
├── requirements.txt       # pandas, openpyxl
├── input/                 # Drop CaseWorthy exports here
├── output/                # Generated reports saved here
├── test_processor.py      # Unit tests for dedup, classification, backlog logic
└── test_e2e.py            # End-to-end smoke test with synthetic data
```

### Data Pipeline
1. **Load** — reads Excel, parses date columns
2. **Dedup** — exact-row dedup, then keeps most recent per Client+Assessment+Program+Type
3. **Classify** — adds `is_signed_off`, `is_pending_review`, `needs_signoff` booleans
4. **Monthly table** — reconstructs point-in-time backlog per office per month
5. **Report** — writes formatted Excel with SUM formulas, conditional coloring, legend

### Key Business Rules
- **Signed off** = `Program Reviewed == "Yes"` AND `Status == "Approved Eligibility Determination"`
- **Pending** = sent back to case manager, not approved, still in backlog
- **Backlog at date D** = began on/before D AND (needs signoff OR signed off after D)
- **Baseline** = August 29, 2025
- Month ranges are auto-detected from data, not hardcoded

## Changelog

### 2026-04-01
- Created CLAUDE.md to track project changes
- Built full assessment_tracker Python app per spec:
  - `config.py` — constants (baseline date, column names, colors, formatting)
  - `processor.py` — load, 2-pass dedup, classification, point-in-time backlog reconstruction, monthly table builder
  - `report_builder.py` — 3-sheet Excel workbook (Summary with formulas, Office Detail, Raw Data)
  - `main.py` — tkinter file picker entry point
  - `requirements.txt` — pandas, openpyxl
  - `test_processor.py` — unit tests validating dedup, classification, backlog logic
  - `test_e2e.py` — end-to-end smoke test with synthetic data
- All processor tests pass; e2e report generation verified
- Added `input/` and `output/` folders; file picker defaults to input, reports save to output
- Added `.gitignore` for pycache and data files
- Fixed chart rendering (restructured to column-based layout)
- Removed Backlog Trend and Monthly Activity chart sheets (not needed)
- Raw Data sheet now only includes report-relevant columns with auto-sized widths
- Summary sheet: added Column Definitions legend and Color Key below data table
  - Definitions merge across full table width with wrap text
  - Updated Pending definition: sent back to case manager for review/changes
- Month headers alternate between dark blue and lighter blue for visual separation

- Added program-to-office mapping in config.py (fallback when CaseWorthy office is missing)
  - CaseWorthy Office Location is used first; mapping fills gaps only
  - 90+ programs mapped to their correct office
  - 12 SSVF-EHA + Bob Woodruff programs excluded from report entirely
  - Added new programs: Sarasota SPEH/Manatee, San Juan SSVF, Charlotte ESG,
    MidFlorida Challenge/Coalition, Orlando ESG, Pasco PSH, Polk ESG, Tampa CDBG
  - Records with unmapped programs go to a "Needs Attention" sheet
  - Needs Attention sheet includes instructions for CaseWorthy cleanup
- Removed "Unassigned" catch-all — office is now determined by program name
- Added tests for exclusion and mapping logic

- Moved program mapping and exclusions to external `program_mapping.xlsx`
  - Mapping sheet: Program Name → Office Location (editable by non-developers)
  - Excluded sheet: programs removed from report entirely
  - config.py now loads mapping at runtime via `load_program_mapping()`
- Added PyInstaller build script (`build_exe.py`)
  - Produces standalone .exe — no Python install needed
  - Copies mapping file, creates input/output folders in dist
  - `get_app_dir()` handles path resolution for both script and exe modes
- Updated HOW_TO_RUN.md with exe instructions and mapping management guide

## Future Plans
- Build and test .exe on Windows with PyInstaller
