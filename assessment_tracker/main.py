import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import sys


def main():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(app_dir, "input")
    output_dir = os.path.join(app_dir, "output")
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

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

    data = process_data(filepath)
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
