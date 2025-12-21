FightAI Portable (Windows)
==========================

Download the repository ZIP from GitHub, unzip it, then open the `FightAI` folder
and double-click `FightAI.cmd`.

The portable layout expects an embedded Python runtime at:
`FightAI/runtime/python/python.exe`.

To keep everything bundled with the repo, the full download should already
include the following files next to `FightAI.cmd`:

- `python-3.11.9-embed-amd64.zip` (Python embeddable runtime)
- `python-3.11.9-amd64.exe` (Python installer, used only to extract Tkinter)

`FightAI.cmd` will bootstrap the embedded runtime from these bundled files and
extract Tkinter so the GUI can launch. This ensures a working Python 3.11
runtime is attached to the repo download even though Python 3.11 is now in
security-only maintenance. If you want to skip this bootstrap step, you can
also provide your own embedded runtime (including Tkinter) in the expected
`FightAI/runtime/python` path.

If neither the embedded runtime nor a system Python is available, install Python
3.10+ and ensure it is on `PATH`.
