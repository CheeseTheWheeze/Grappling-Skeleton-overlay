@echo off
setlocal

set "BASE_DIR=%~dp0"
set "PYTHONHOME=%BASE_DIR%runtime\python"
set "PYTHONPATH=%BASE_DIR%app"
set "FIGHTAI_DATA_DIR=%BASE_DIR%FightAI_Data"
set "GSO_DATA_DIR=%BASE_DIR%FightAI_Data"

if not exist "%BASE_DIR%runtime\python\python.exe" (
  echo Missing Python runtime at "%BASE_DIR%runtime\python\python.exe".
  echo Run "%BASE_DIR%tools\bootstrap_python.ps1" to install the runtime, then retry.
  exit /b 1
)

"%BASE_DIR%runtime\python\python.exe" -m gso_app.entrypoint
endlocal
