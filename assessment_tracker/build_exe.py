"""Build script to package the Assessment Tracker as a standalone .exe.

Usage:
    python build_exe.py

Requirements:
    pip install pyinstaller

Output:
    dist/Assessment_Tracker/
        Assessment_Tracker.exe
        program_mapping.xlsx   (copied automatically)
        input/                 (created automatically)
        output/                (created automatically)

The entire dist/Assessment_Tracker/ folder is what you distribute.
"""
import subprocess
import shutil
import os
import sys

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(APP_DIR, "dist", "Assessment_Tracker")


def build():
    print("=" * 60)
    print("Building Assessment Tracker .exe")
    print("=" * 60)

    # Run PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "Assessment_Tracker",
        "--onefile",
        "--windowed",
        "--distpath", os.path.join(APP_DIR, "dist"),
        "--workpath", os.path.join(APP_DIR, "build"),
        "--specpath", APP_DIR,
        os.path.join(APP_DIR, "main.py"),
    ]
    print(f"\nRunning: {' '.join(cmd)}\n")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("\nERROR: PyInstaller build failed.")
        sys.exit(1)

    # Create distribution folder structure
    os.makedirs(DIST_DIR, exist_ok=True)

    # Move the exe into the folder
    exe_name = "Assessment_Tracker.exe" if os.name == "nt" else "Assessment_Tracker"
    exe_src = os.path.join(APP_DIR, "dist", exe_name)
    exe_dst = os.path.join(DIST_DIR, exe_name)
    if os.path.exists(exe_src) and exe_src != exe_dst:
        shutil.move(exe_src, exe_dst)

    # Copy the mapping file
    mapping_src = os.path.join(APP_DIR, "program_mapping.xlsx")
    if os.path.exists(mapping_src):
        shutil.copy2(mapping_src, os.path.join(DIST_DIR, "program_mapping.xlsx"))
        print(f"  Copied program_mapping.xlsx")
    else:
        print(f"  WARNING: {mapping_src} not found — you'll need to add it manually")

    # Create input/output folders
    os.makedirs(os.path.join(DIST_DIR, "input"), exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "output"), exist_ok=True)

    print(f"\n{'=' * 60}")
    print(f"BUILD COMPLETE")
    print(f"{'=' * 60}")
    print(f"\nDistribution folder: {DIST_DIR}")
    print(f"Contents:")
    for item in sorted(os.listdir(DIST_DIR)):
        print(f"  {item}")
    print(f"\nTo distribute: zip the entire Assessment_Tracker/ folder.")


if __name__ == "__main__":
    build()
