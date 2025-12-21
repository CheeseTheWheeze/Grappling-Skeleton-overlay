FightAI Portable
=================

1) The portable layout prefers the embedded Python runtime at:
   FightAI\runtime\python\python.exe

2) If the embedded runtime is missing, bundle the following files next to
   FightAI.cmd before launching:
   - python-3.11.9-embed-amd64.zip
   - python-3.11.9-amd64.exe

   FightAI.cmd will configure the embeddable runtime in FightAI\runtime\python
   and extract Tkinter GUI components from the bundled installer.

3) If the embedded runtime is missing and no system Python is available on PATH,
   install Python 3.10+ and ensure it is on PATH.

4) Launch the app by double-clicking FightAI.cmd.

If you supply a FightAI.exe launcher, it can be used instead of FightAI.cmd.
