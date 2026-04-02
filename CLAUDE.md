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

### 2026-04-02
- Replaced bare file picker with full GUI application window
  - Input file browser, output folder selector, mapping status indicator
  - Progress bar with threaded processing (UI stays responsive)
  - Generate Report button, success/error dialogs
  - Footer credit line
- Rebuilt as standalone .exe via PyInstaller

## Future Plans
- Build and test .exe on Windows with PyInstaller

---

## GUI App Design Reference

Reusable pattern for building similar tkinter data-processing apps.
Copy this structure and adapt the fields/processing logic.

### Layout Structure

```
┌─────────────────────────────────────────────────┐
│  HEADER (accent color banner)                   │
│    Title — large bold white text                │
│    Subtitle — lighter, smaller text             │
├─────────────────────────────────────────────────┤
│  BODY (light background, padded)                │
│                                                 │
│  Input File Label (bold)                        │
│  [ text entry field          ] [Browse...]      │
│                                                 │
│  Output Folder Label (bold)                     │
│  [ text entry field          ] [Browse...]      │
│                                                 │
│  Status indicator (green check / warning)       │
│                                                 │
│  [========= progress bar =========]             │
│  Status text ("Ready" / "Processing...")        │
│                                                 │
│                        [ Generate Report ]      │
├─────────────────────────────────────────────────┤
│  FOOTER (subtle background)                     │
│    Credit / version text (italic, small)        │
└─────────────────────────────────────────────────┘
```

### Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Header / accent / primary button | Dark blue | `#1F4E79` |
| Button hover / active | Medium blue | `#2E75B6` |
| Body background | Light gray-blue | `#F0F4F8` |
| Footer background | Slightly darker gray | `#E8EDF2` |
| Success text | Green | `#2E7D32` |
| Error / warning text | Red | `#C62828` |
| Muted text (status, footer) | Gray | `#555` / `#666` |

### Fonts

| Element | Font |
|---------|------|
| Title | `("Segoe UI", 16, "bold")` |
| Subtitle | `("Segoe UI", 10)` |
| Section labels | `("Segoe UI", 10, "bold")` |
| Input fields / body text | `("Segoe UI", 9)` |
| Button text | `("Segoe UI", 11, "bold")` |
| Footer | `("Segoe UI", 8, "italic")` |

### Key Implementation Details

**Window setup:**
```python
root = tk.Tk()
root.title("App Title")
root.resizable(False, False)
root.configure(bg="#F0F4F8")
```

**Header (accent banner):**
```python
header = tk.Frame(root, bg="#1F4E79", padx=20, pady=14)
header.pack(fill="x")
tk.Label(header, text="App Title",
         font=("Segoe UI", 16, "bold"), fg="white", bg="#1F4E79").pack()
tk.Label(header, text="Subtitle description",
         font=("Segoe UI", 10), fg="#B0C4DE", bg="#1F4E79").pack()
```

**Browse row pattern (input file or output folder):**
```python
tk.Label(body, text="Label:", font=("Segoe UI", 10, "bold"),
         bg=bg, anchor="w").grid(row=R, column=0, columnspan=2, sticky="w")
frame = tk.Frame(body, bg=bg)
frame.grid(row=R+1, column=0, columnspan=2, sticky="ew")
var = tk.StringVar()
tk.Entry(frame, textvariable=var, width=52, font=("Segoe UI", 9)).pack(side="left", padx=(0, 8))
tk.Button(frame, text="Browse...", command=browse_fn, font=("Segoe UI", 9)).pack(side="left")
```

**Progress bar + status:**
```python
progress = ttk.Progressbar(body, mode="indeterminate", length=380)
progress.grid(...)
status_var = tk.StringVar(value="Ready")
tk.Label(body, textvariable=status_var, font=("Segoe UI", 9), bg=bg, fg="#555").grid(...)
# Start: progress.start(15)
# Stop:  progress.stop()
```

**Primary action button (right-aligned):**
```python
btn = tk.Button(frame, text="Generate Report",
                command=run_fn, font=("Segoe UI", 11, "bold"),
                bg="#1F4E79", fg="white", padx=20, pady=6,
                activebackground="#2E75B6", activeforeground="white")
btn.pack(side="right")
```

**Footer:**
```python
footer = tk.Frame(root, bg="#E8EDF2", padx=20, pady=8)
footer.pack(fill="x", side="bottom")
tk.Label(footer, text="Credit line here",
         font=("Segoe UI", 8, "italic"), fg="#666", bg="#E8EDF2").pack()
```

**Threaded processing (keeps UI responsive):**
```python
def _run(self):
    self.run_btn.config(state="disabled")
    self.progress.start(15)
    self.status_var.set("Processing...")
    thread = threading.Thread(target=self._process, args=(...,), daemon=True)
    thread.start()

def _process(self, ...):
    try:
        # ... do work ...
        self.root.after(0, self._on_success, result)
    except Exception as e:
        self.root.after(0, self._on_error, str(e))

def _on_success(self, result):
    self.progress.stop()
    self.status_var.set("Done")
    self.run_btn.config(state="normal")
    messagebox.askyesno("Done", "Open the result?")

def _on_error(self, msg):
    self.progress.stop()
    self.status_var.set("Error")
    self.run_btn.config(state="normal")
    messagebox.showerror("Error", msg)
```

### PyInstaller Build

```python
# build_exe.py key flags:
"--onefile"     # single .exe
"--windowed"    # no console window (GUI app)
"--name", "App_Name"
```

After build, copy config files (xlsx, json, etc.) next to the exe.
Use `get_app_dir()` to resolve paths at runtime:
```python
def get_app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)  # PyInstaller exe
    return os.path.dirname(os.path.abspath(__file__))  # normal script
```
