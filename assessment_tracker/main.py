import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import sys


def main():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(
        title="Select CaseWorthy Export",
        filetypes=[("Excel files", "*.xlsx *.xls")],
    )
    if not filepath:
        print("No file selected.")
        return

    print(f"Processing: {filepath}")
    from processor import process_data
    from report_builder import build_report

    data = process_data(filepath)
    output_dir = os.path.dirname(filepath)
    output_path = build_report(data, output_dir=output_dir)

    print(f"Report saved: {output_path}")
    if os.name == "nt":
        os.startfile(output_path)
    elif sys.platform == "darwin":
        subprocess.run(["open", output_path])
    else:
        subprocess.run(["xdg-open", output_path])


if __name__ == "__main__":
    main()
