@echo off
setlocal

set "BASE_DIR=%~dp0"
set "LOG_PATH=%USERPROFILE%\Desktop\GrapplingPipelineCodexLog.txt"

echo Running repair/bootstrap. Logs will be written to "%LOG_PATH%".
call "%BASE_DIR%tools\bootstrap_python.cmd" -EnsurePth
if errorlevel 1 (
  echo Repair failed. See "%LOG_PATH%" for details.
  pause
  exit /b 1
)

echo Repair complete. You can now run FightAI.vbs.
pause

endlocal
