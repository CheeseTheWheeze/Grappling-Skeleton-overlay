@echo off
setlocal
set SCRIPT_DIR=%~dp0
set REPO_ROOT=%SCRIPT_DIR%

python "%REPO_ROOT%apps/windows/main.py"
if errorlevel 1 (
  echo Day-1 run failed.
  exit /b 1
)

python "%REPO_ROOT%tests/day1_validate.py"
if errorlevel 1 (
  echo Day-1 validation failed.
  echo.
  pause
  exit /b 1
)

echo Day-1 test complete.
echo.
pause
