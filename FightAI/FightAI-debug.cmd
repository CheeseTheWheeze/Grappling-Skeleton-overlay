@echo off
setlocal

set "BASE_DIR=%~dp0"
set "LOG_PATH=%USERPROFILE%\Desktop\GrapplingPipelineCodexLog.txt"

echo Debug launch. Logs will be written to "%LOG_PATH%".
call "%BASE_DIR%FightAI.cmd"

endlocal
