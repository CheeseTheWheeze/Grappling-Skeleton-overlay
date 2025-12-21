# Quickstart

## Launch the app

1. Open the `FightAI/` folder.
2. Run the launcher at [`FightAI/FightAI.vbs`](FightAI/FightAI.vbs) (or
   [`FightAI/FightAI-debug.cmd`](FightAI/FightAI-debug.cmd) if you want a console).

> **Required runtime path:** the launcher expects the embedded Python runtime at
> `FightAI/runtime/python/python.exe`.

On first launch, the bootstrapper downloads the runtime automatically. If the
download fails, rerun [`FightAI/tools/bootstrap_python.ps1`](FightAI/tools/bootstrap_python.ps1).

Every launch writes a log to your Desktop named `GrapplingPipelineCodexLog.txt`
(overwrites on each run).

## Repository layout

- **`FightAI/`**: Portable Windows app bundle, launcher (`FightAI.cmd`), runtime,
  and app data.
- **`src/`**: Source code for the application and supporting scripts.
- **`models/`**: Model files and related assets used by the app.
- **`tools/`**: Developer tooling and helper scripts for maintenance or setup.

For more details about the portable bundle, see
[`FightAI/README.txt`](FightAI/README.txt).
