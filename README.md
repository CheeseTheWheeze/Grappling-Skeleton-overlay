FightAI Portable (Windows)
==========================

Download the repository ZIP from GitHub, unzip it, then open the `FightAI` folder
and double-click `FightAI.cmd`.

The portable layout expects an embedded Python runtime at:
`FightAI/runtime/python/python.exe`.

If that runtime is not present, `FightAI.cmd` will automatically download the
Python embeddable runtime into `FightAI/runtime/python`, then extract the
Tkinter GUI components from the standard installer so the launcher can open.
If you want to skip the download, you can also provide your own embedded
runtime (including Tkinter) in that path.

If neither the embedded runtime nor a system Python is available, install Python
3.10+ and ensure it is on `PATH`.
