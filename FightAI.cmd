@echo off
setlocal

set "BASE_DIR=%~dp0"
set "APP_DIR=%BASE_DIR%FightAI"
set "PYTHONHOME=%APP_DIR%\runtime\python"
set "PYTHONPATH=%APP_DIR%\app"
set "FIGHTAI_DATA_DIR=%APP_DIR%\FightAI_Data"
set "GSO_DATA_DIR=%APP_DIR%\FightAI_Data"

if not exist "%APP_DIR%\runtime\python\python.exe" (
  echo ERROR: Missing embedded Python runtime at:
  echo   %APP_DIR%\runtime\python\python.exe
  echo.
  echo Re-download the portable package or restore the runtime folder.
  pause
  exit /b 1
)

"%APP_DIR%\runtime\python\python.exe" -m gso_app.entrypoint
if errorlevel 1 (
  echo.
  echo ERROR: FightAI exited with an error.
  pause
  exit /b 1
)
endlocal
