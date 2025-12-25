FightAI Portable
=================

1) Launch the app by double-clicking FightAI.vbs (or FightAI-debug.cmd).

2) On first launch, the embedded Python runtime is downloaded automatically to:
   FightAI\runtime\python\python.exe

   If the embedded runtime cannot be installed, the launcher falls back to a
   system Python (if available).

3) Each launch writes a log to your Desktop named:
   GrapplingPipelineCodexLog.txt

4) If the app still fails to launch, run FightAI-repair.cmd to repair the
   embedded runtime and update the import paths.

If you supply a FightAI.exe launcher, it can be used instead of FightAI.cmd.
