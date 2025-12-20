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
  echo Fix options:
  echo   [1] Open the runtime folder to verify files.
  echo   [2] Open the setup instructions (README).
  echo   [3] Exit.
  echo.
  choice /c 123 /n /m "Choose 1, 2, or 3: "
  if errorlevel 3 goto :end
  if errorlevel 2 (
    start "" "%BASE_DIR%README.md"
    goto :end
  )
  start "" "%APP_DIR%\runtime"
  goto :end
)

"%APP_DIR%\runtime\python\python.exe" -m gso_app.entrypoint
if errorlevel 1 (
  echo.
  echo ERROR: FightAI exited with an error.
  echo.
  echo Fix options:
  echo   [1] Open the data folder (FightAI_Data).
  echo   [2] Open the app folder.
  echo   [3] Open the setup instructions (README).
  echo   [4] Exit.
  echo.
  choice /c 1234 /n /m "Choose 1, 2, 3, or 4: "
  if errorlevel 4 goto :end
  if errorlevel 3 (
    start "" "%BASE_DIR%README.md"
    goto :end
  )
  if errorlevel 2 (
    start "" "%APP_DIR%\app"
    goto :end
  )
  start "" "%APP_DIR%\FightAI_Data"
  goto :end
)

:end
endlocal
