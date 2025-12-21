FightAI Portable
=================

1) The portable layout prefers the embedded Python runtime at:
   FightAI\runtime\python\python.exe

2) If the embedded runtime is missing, FightAI.cmd will automatically download
   and configure the Python embeddable runtime in FightAI\runtime\python, then
   extract Tkinter GUI components from the official installer.

3) If the embedded runtime is missing and no system Python is available on PATH,
   install Python 3.10+ and ensure it is on PATH.

4) Launch the app by double-clicking FightAI.cmd.

If you supply a FightAI.exe launcher, it can be used instead of FightAI.cmd.
