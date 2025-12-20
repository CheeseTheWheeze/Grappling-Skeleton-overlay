@echo off
setlocal

set "BASE_DIR=%~dp0"
set "APP_DIR=%BASE_DIR%FightAI\"
set "PYTHONHOME=%APP_DIR%runtime\python"
set "PYTHONPATH=%APP_DIR%app"
set "FIGHTAI_DATA_DIR=%APP_DIR%FightAI_Data"
set "GSO_DATA_DIR=%APP_DIR%FightAI_Data"

"%APP_DIR%runtime\python\python.exe" -m gso_app.entrypoint
endlocal
