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

set "PYTHON_LAUNCHER="
set "PYTHON_ARGS="

call "%BASE_DIR%tools\bootstrap_python.cmd" -EnsurePth
set "BOOTSTRAP_ERROR=%ERRORLEVEL%"
if not "%BOOTSTRAP_ERROR%"=="0" (
  >> "%LOG_PATH%" echo [%DATE% %TIME%] Bootstrap encountered an error.
)

if not exist "%BASE_DIR%runtime\python\python.exe" (
  if not "%BOOTSTRAP_ERROR%"=="0" (
    echo Missing Python runtime at "%BASE_DIR%runtime\python\python.exe".
    echo Bootstrap failed. Falling back to system Python if available.
    >> "%LOG_PATH%" echo [%DATE% %TIME%] Bootstrap failed for runtime at "%BASE_DIR%runtime\python\python.exe".
  )
)

if exist "%BASE_DIR%runtime\python\python.exe" (
  set "PYTHON_LAUNCHER=%BASE_DIR%runtime\python\python.exe"
)

if not defined PYTHON_LAUNCHER (
  where py >nul 2>&1
  if not errorlevel 1 (
    set "PYTHON_LAUNCHER=py"
    set "PYTHON_ARGS=-3.11"
  )
)

if not defined PYTHON_LAUNCHER (
  where python >nul 2>&1
  if not errorlevel 1 (
    set "PYTHON_LAUNCHER=python"
  )
)

if not defined PYTHON_LAUNCHER (
  echo No Python runtime found. See "%LOG_PATH%" for details.
  >> "%LOG_PATH%" echo [%DATE% %TIME%] No Python runtime found. Checked embedded, py launcher, and PATH.
  call "%BASE_DIR%tools\write_support_prompt.cmd" >> "%LOG_PATH%"
  popd
  exit /b 1
)

>> "%LOG_PATH%" echo [%DATE% %TIME%] Using Python launcher: %PYTHON_LAUNCHER% %PYTHON_ARGS%
"%PYTHON_LAUNCHER%" %PYTHON_ARGS% -m gso_app.entrypoint >> "%LOG_PATH%" 2>&1
if errorlevel 1 (
  >> "%LOG_PATH%" echo [%DATE% %TIME%] Launch failed.
  call "%BASE_DIR%tools\write_support_prompt.cmd" >> "%LOG_PATH%"
  echo Launch failed. See "%LOG_PATH%" for details.
  pause
)
popd
endlocal
