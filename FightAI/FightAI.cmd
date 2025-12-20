@echo off
setlocal

set "BASE_DIR=%~dp0"
set "PYTHONHOME=%BASE_DIR%runtime\python"
set "PYTHONPATH=%BASE_DIR%app"
set "FIGHTAI_DATA_DIR=%BASE_DIR%FightAI_Data"
set "GSO_DATA_DIR=%BASE_DIR%FightAI_Data"

"%BASE_DIR%runtime\python\python.exe" -m gso_app.entrypoint
endlocal
