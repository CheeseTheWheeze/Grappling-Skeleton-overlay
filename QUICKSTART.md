# Quickstart

## Launch the app

1. Open the `FightAI/` folder.
2. Run the launcher at [`FightAI/FightAI.cmd`](FightAI/FightAI.cmd).

> **Required runtime path:** the launcher expects the embedded Python runtime at
> `FightAI/runtime/python/python.exe`.

If you have not downloaded the embedded runtime yet, run the bootstrap script at
[`FightAI/tools/bootstrap_python.ps1`](FightAI/tools/bootstrap_python.ps1), then
launch `FightAI/FightAI.cmd` again.

## Repository layout

- **`FightAI/`**: Portable Windows app bundle, launcher (`FightAI.cmd`), runtime,
  and app data.
- **`src/`**: Source code for the application and supporting scripts.
- **`models/`**: Model files and related assets used by the app.
- **`tools/`**: Developer tooling and helper scripts for maintenance or setup.

For more details about the portable bundle, see
[`FightAI/README.txt`](FightAI/README.txt).
