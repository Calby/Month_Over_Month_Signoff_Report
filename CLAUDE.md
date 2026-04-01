# CLAUDE.md - Project Changelog & Notes

## Project: Month Over Month Signoff Report

## Changelog

### 2026-04-01
- Created CLAUDE.md to track project changes
- Built full assessment_tracker Python app per spec:
  - `config.py` — constants (baseline date, column names, colors, formatting)
  - `processor.py` — load, 2-pass dedup, classification (signed_off/pending/needs_signoff), point-in-time backlog reconstruction, monthly table builder
  - `report_builder.py` — 5-sheet Excel workbook (Summary with formulas, Backlog Trend chart, Monthly Activity chart, Office Detail, Raw Data)
  - `main.py` — tkinter file picker entry point
  - `requirements.txt` — pandas, openpyxl
  - `test_processor.py` — unit tests validating dedup, classification, backlog logic
  - `test_e2e.py` — end-to-end smoke test with synthetic data
- All processor tests pass; e2e report generation verified
