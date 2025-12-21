@echo off
setlocal

set "BASE_DIR=%~dp0"
set "PYTHONPATH=%BASE_DIR%app"
set "FIGHTAI_DATA_DIR=%BASE_DIR%FightAI_Data"
set "GSO_DATA_DIR=%BASE_DIR%FightAI_Data"
set "PYTHONUTF8=1"

set "EMBEDDED_PYTHON=%BASE_DIR%runtime\python\python.exe"

if not exist "%EMBEDDED_PYTHON%" (
    echo Embedded Python not found. Bootstrapping runtime from bundled files...
    powershell -NoProfile -ExecutionPolicy Bypass -File "%BASE_DIR%setup_python.ps1"
    if errorlevel 1 (
        echo Failed to setup embedded Python. Ensure the Python embeddable zip and installer are bundled next to FightAI.cmd.
    )
)

if exist "%EMBEDDED_PYTHON%" (
    set "PYTHONHOME=%BASE_DIR%runtime\python"
    "%EMBEDDED_PYTHON%" -m gso_app.entrypoint
    endlocal
    exit /b %errorlevel%
)

where python >nul 2>nul
if errorlevel 1 (
    echo Embedded Python not found and no system Python available in PATH.
    echo Please install Python 3.10+ or add it to PATH.
    endlocal
    exit /b 1
)

set "PYTHONHOME="
python -m gso_app.entrypoint
endlocal
