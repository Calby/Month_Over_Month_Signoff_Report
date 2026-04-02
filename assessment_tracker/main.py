import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import subprocess
import os
import sys

from config import get_app_dir, MAPPING_FILENAME


class AssessmentTrackerApp:
    def __init__(self):
        self.app_dir = get_app_dir()
        self.input_dir = os.path.join(self.app_dir, "input")
        self.output_dir = os.path.join(self.app_dir, "output")
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        self.mapping_path = os.path.join(self.app_dir, MAPPING_FILENAME)

        self.root = tk.Tk()
        self.root.title("Assessment Sign-Off Backlog Tracker")
        self.root.resizable(False, False)

        # Colors
        bg = "#F0F4F8"
        accent = "#1F4E79"
        self.root.configure(bg=bg)

        # --- Header ---
        header = tk.Frame(self.root, bg=accent, padx=20, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="Assessment Sign-Off Backlog Tracker",
                 font=("Segoe UI", 16, "bold"), fg="white", bg=accent).pack()
        tk.Label(header, text="CaseWorthy Export \u2192 Monthly Backlog Report",
                 font=("Segoe UI", 10), fg="#B0C4DE", bg=accent).pack()

        # --- Main content ---
        body = tk.Frame(self.root, bg=bg, padx=24, pady=16)
        body.pack(fill="both")

        # Input file
        tk.Label(body, text="CaseWorthy Export File:", font=("Segoe UI", 10, "bold"),
                 bg=bg, anchor="w").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))
        input_frame = tk.Frame(body, bg=bg)
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var,
                                    width=52, font=("Segoe UI", 9))
        self.input_entry.pack(side="left", padx=(0, 8))
        tk.Button(input_frame, text="Browse...", command=self._browse_input,
                  font=("Segoe UI", 9)).pack(side="left")

        # Output location
        tk.Label(body, text="Output Folder (optional):", font=("Segoe UI", 10, "bold"),
                 bg=bg, anchor="w").grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 4))
        output_frame = tk.Frame(body, bg=bg)
        output_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.output_var = tk.StringVar(value=self.output_dir)
        self.output_entry = tk.Entry(output_frame, textvariable=self.output_var,
                                     width=52, font=("Segoe UI", 9))
        self.output_entry.pack(side="left", padx=(0, 8))
        tk.Button(output_frame, text="Browse...", command=self._browse_output,
                  font=("Segoe UI", 9)).pack(side="left")

        # Mapping status
        mapping_exists = os.path.exists(self.mapping_path)
        status_text = ("\u2705  program_mapping.xlsx found" if mapping_exists
                       else "\u26A0\uFE0F  program_mapping.xlsx not found — all programs will need attention")
        status_color = "#2E7D32" if mapping_exists else "#C62828"
        tk.Label(body, text=status_text, font=("Segoe UI", 9), fg=status_color,
                 bg=bg).grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 12))

        # Progress
        self.progress = ttk.Progressbar(body, mode="indeterminate", length=380)
        self.progress.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 4))
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(body, textvariable=self.status_var,
                                     font=("Segoe UI", 9), bg=bg, fg="#555")
        self.status_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 12))

        # Buttons
        btn_frame = tk.Frame(body, bg=bg)
        btn_frame.grid(row=7, column=0, columnspan=2, sticky="e", pady=(0, 4))
        self.run_btn = tk.Button(btn_frame, text="Generate Report",
                                 command=self._run, font=("Segoe UI", 11, "bold"),
                                 bg=accent, fg="white", padx=20, pady=6,
                                 activebackground="#2E75B6", activeforeground="white")
        self.run_btn.pack(side="right")

        # --- Footer ---
        footer = tk.Frame(self.root, bg="#E8EDF2", padx=20, pady=8)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer,
                 text="Crafted by the legendary James Calby \u2014 Data Systems Analyst Extraordinaire \u2728",
                 font=("Segoe UI", 8, "italic"), fg="#666", bg="#E8EDF2").pack()

    def _browse_input(self):
        path = filedialog.askopenfilename(
            title="Select CaseWorthy Export",
            initialdir=self.input_dir,
            filetypes=[("Excel files", "*.xlsx *.xls")],
        )
        if path:
            self.input_var.set(path)

    def _browse_output(self):
        path = filedialog.askdirectory(
            title="Select Output Folder",
            initialdir=self.output_dir,
        )
        if path:
            self.output_var.set(path)

    def _run(self):
        filepath = self.input_var.get().strip()
        if not filepath:
            messagebox.showwarning("No File Selected",
                                   "Please select a CaseWorthy export file first.")
            return
        if not os.path.exists(filepath):
            messagebox.showerror("File Not Found", f"Cannot find:\n{filepath}")
            return

        output_dir = self.output_var.get().strip() or self.output_dir
        self.run_btn.config(state="disabled")
        self.progress.start(15)
        self.status_var.set("Processing...")

        thread = threading.Thread(target=self._process, args=(filepath, output_dir),
                                  daemon=True)
        thread.start()

    def _process(self, filepath, output_dir):
        try:
            from processor import process_data
            from report_builder import build_report

            data = process_data(filepath, mapping_path=self.mapping_path)
            output_path = build_report(data, output_dir=output_dir)

            self.root.after(0, self._on_success, output_path)
        except Exception as e:
            self.root.after(0, self._on_error, str(e))

    def _on_success(self, output_path):
        self.progress.stop()
        self.status_var.set(f"Report saved: {os.path.basename(output_path)}")
        self.run_btn.config(state="normal")

        if messagebox.askyesno("Report Generated",
                               f"Report saved to:\n{output_path}\n\nOpen it now?"):
            if os.name == "nt":
                os.startfile(output_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", output_path])
            else:
                subprocess.run(["xdg-open", output_path])

    def _on_error(self, error_msg):
        self.progress.stop()
        self.status_var.set("Error — see details")
        self.run_btn.config(state="normal")
        messagebox.showerror("Processing Error",
                             f"Something went wrong:\n\n{error_msg}")

    def run(self):
        self.root.mainloop()


def main():
    app = AssessmentTrackerApp()
    app.run()


if __name__ == "__main__":
    main()
