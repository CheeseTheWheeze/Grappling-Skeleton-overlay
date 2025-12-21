@echo off
setlocal

set "BASE_DIR=%~dp0.."
set "PYTHON_EXE=%BASE_DIR%runtime\python\python.exe"
set "LOG_PATH=%USERPROFILE%\Desktop\GrapplingPipelineCodexLog.txt"

echo ======= SUPPORT PROMPT =======
echo Paste the following into chat:
echo OS: %OS%
echo User: %USERNAME%
echo Base dir: %BASE_DIR%
if exist "%PYTHON_EXE%" (
  for /f "delims=" %%v in ('"%PYTHON_EXE%" -V 2^>^&1') do echo Python: %%v
) else (
  echo Python: missing at %PYTHON_EXE%
)
echo Log path: %LOG_PATH%
echo Last 50 lines of log:
if exist "%LOG_PATH%" (
  where powershell.exe >nul 2>&1
  if errorlevel 1 (
    echo PowerShell missing. Please open the log manually.
  ) else (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Content -Path '%LOG_PATH%' -Tail 50"
  )
) else (
  echo Log file not found.
)
echo ======= END =======

endlocal
