# Grappling-Skeleton-overlay

A simple video-analysis tool with a friendly GUI. This guide is written so anyone can
set it up and use it without technical experience.

---

## Quick Start (recommended)

Follow these steps exactly. You only have to do this once.

### 1) Download the project

If you already have the folder on your computer, skip to step 2.

1. Open this GitHub page in your browser.
2. Click **Code** ➜ **Download ZIP**.
3. Unzip the download.
4. Open the unzipped folder.

### 2) Install the app and create the Desktop icon

1. Open a terminal:
   - **Windows:** Start menu ➜ type **PowerShell** ➜ open it.
   - **macOS:** Applications ➜ Utilities ➜ **Terminal**.
   - **Linux:** Open **Terminal** from your apps.
2. In the terminal, go to the project folder:

   ```bash
   cd /path/to/Grappling-Skeleton-overlay
   ```

   Tip: If you dragged the folder onto the terminal window, it will fill in the path for you.

3. Run the installer:

   ```bash
   pip install -e .
   gso install
   ```

✅ You should now see a **GSO Analyzer** icon on your Desktop.

---

## Everyday Use (GUI)

1. Double‑click **GSO Analyzer** on your Desktop.
2. Click **Browse** and pick a video.
3. Choose where you want the output files to go.
4. Click **Run / Generate**.

The app will create these files in your output folder:
- `summary.txt`
- `metrics.json`
- `analysis.json`

---

## If the Desktop Icon Doesn’t Work

1. Open a terminal in the project folder (see step 2 above).
2. Run:

   ```bash
   gso install
   ```

This fixes missing or broken installs by re‑checking requirements and rebuilding the launcher.

---

## Optional: Command Line (advanced)

Only use this if you are comfortable with the terminal.

### Analyze a video directly

```bash
gso analyze --input /path/to/video.mp4 --output ./artifacts
```

### Run the GUI without the desktop icon

```bash
gso gui
```

---

## Troubleshooting

**“gso: command not found”**
- Make sure you ran:

  ```bash
  pip install -e .
  ```

**Python version errors**
- You need Python **3.9 or newer**.

**I want a clean reinstall**
- Run this in the project folder:

  ```bash
  gso install
  ```

---

## What gets created on your computer

- A configuration folder: `~/.gso`
- A Desktop launcher: **GSO Analyzer** (numbered versions are kept if you reinstall)
