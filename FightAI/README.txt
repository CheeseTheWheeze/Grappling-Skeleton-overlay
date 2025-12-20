FightAI Portable
=================

1) The portable layout prefers the embedded Python runtime at:
   FightAI\runtime\python\python.exe

2) If the embedded runtime is missing, FightAI.cmd will look for a system
   Python on PATH and run:
   python -m gso_app.entrypoint
   with PYTHONPATH set to FightAI\app.

3) Launch the app by double-clicking FightAI.cmd.

If you supply a FightAI.exe launcher, it can be used instead of FightAI.cmd.
