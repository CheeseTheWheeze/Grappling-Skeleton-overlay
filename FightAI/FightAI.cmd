@echo off
setlocal

set "BASE_DIR=%~dp0"
set "PYTHONHOME=%BASE_DIR%runtime\python"
set "PYTHONPATH=%BASE_DIR%app"
set "FIGHTAI_DATA_DIR=%BASE_DIR%FightAI_Data"
set "GSO_DATA_DIR=%BASE_DIR%FightAI_Data"

pushd "%BASE_DIR%"

set "LOG_PATH=%USERPROFILE%\Desktop\GrapplingPipelineCodexLog.txt"
> "%LOG_PATH%" echo [%DATE% %TIME%] Launch start
>> "%LOG_PATH%" echo Base dir: %BASE_DIR%
>> "%LOG_PATH%" echo Runtime: %BASE_DIR%runtime\python\python.exe

if not exist "%BASE_DIR%runtime\python\python.exe" (
  call "%BASE_DIR%tools\bootstrap_python.cmd" || (
    echo Missing Python runtime at "%BASE_DIR%runtime\python\python.exe".
    echo Bootstrap failed. Run "%BASE_DIR%tools\bootstrap_python.ps1" manually to retry.
    >> "%LOG_PATH%" echo [%DATE% %TIME%] Bootstrap failed for runtime at "%BASE_DIR%runtime\python\python.exe".
    call "%BASE_DIR%tools\write_support_prompt.cmd" >> "%LOG_PATH%"
    popd
    exit /b 1
  )
)

"%BASE_DIR%runtime\python\python.exe" -m gso_app.entrypoint >> "%LOG_PATH%" 2>&1
if errorlevel 1 (
  >> "%LOG_PATH%" echo [%DATE% %TIME%] Launch failed.
  call "%BASE_DIR%tools\write_support_prompt.cmd" >> "%LOG_PATH%"
  echo Launch failed. See "%LOG_PATH%" for details.
  pause
)
popd
endlocal
