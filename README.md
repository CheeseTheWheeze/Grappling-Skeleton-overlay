FightAI Portable (Windows)
==========================

Download the repository ZIP from GitHub, unzip it, then open the `FightAI` folder
and double-click `FightAI.cmd`.

The portable layout expects an embedded Python runtime at:
`FightAI/runtime/python/python.exe`.
If that runtime is not present, `FightAI.cmd` will fall back to a system Python
found on `PATH` and run `python -m gso_app.entrypoint` with `PYTHONPATH` set to
`FightAI/app`.

If neither the embedded runtime nor a system Python is available, install Python
3.10+ and ensure it is on `PATH`.
