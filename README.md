FightAI Portable (Windows)
==========================

Download the repository ZIP from GitHub, unzip it, then open the `FightAI` folder
and double-click `FightAI.vbs` (or `FightAI-debug.cmd` if you want a console).

On first launch, the app automatically downloads and unpacks the embedded
Python 3.11 runtime into `FightAI/runtime/python`. No manual Python install is
required.

Every launch writes a log to your Desktop named
`GrapplingPipelineCodexLog.txt` (overwrites on each run).

## Platform roadmap

- **Windows (today):** portable bundle with an embedded Python runtime.
- **macOS (planned):** ship a signed `.app` bundle with Python embedded
  (likely via PyInstaller/Nuitka).
- **Mobile (planned):** package as a native wrapper with embedded runtime
  and models (platform-specific).
