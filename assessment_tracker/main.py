import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import sys

from config import get_app_dir, MAPPING_FILENAME


def main():
    app_dir = get_app_dir()
    input_dir = os.path.join(app_dir, "input")
    output_dir = os.path.join(app_dir, "output")
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Verify mapping file exists
    mapping_path = os.path.join(app_dir, MAPPING_FILENAME)
    if not os.path.exists(mapping_path):
        print(f"WARNING: {MAPPING_FILENAME} not found in {app_dir}")
        print("  The report will flag all programs as 'Needs Attention'.")
        print(f"  Place {MAPPING_FILENAME} next to the application to fix this.\n")

    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(
        title="Select CaseWorthy Export",
        initialdir=input_dir,
        filetypes=[("Excel files", "*.xlsx *.xls")],
    )
    if not filepath:
        print("No file selected.")
        return

    print(f"Processing: {filepath}")
    from processor import process_data
    from report_builder import build_report

    data = process_data(filepath, mapping_path=mapping_path)
    output_path = build_report(data, output_dir=output_dir)

    print(f"\nReport saved: {output_path}")
    if os.name == "nt":
        os.startfile(output_path)
    elif sys.platform == "darwin":
        subprocess.run(["open", output_path])
    else:
        subprocess.run(["xdg-open", output_path])


if __name__ == "__main__":
    main()
