@echo off
setlocal

set "BASE_DIR=%~dp0.."
set "PS_SCRIPT=%BASE_DIR%tools\bootstrap_python.ps1"

where powershell.exe >nul 2>&1
if errorlevel 1 (
  echo PowerShell is required to download the embedded Python runtime.
  exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%" -LogPath "%USERPROFILE%\\Desktop\\GrapplingPipelineCodexLog.txt"
if errorlevel 1 (
  exit /b 1
)

if not exist "%BASE_DIR%runtime\python\python.exe" (
  echo Embedded Python runtime was not installed correctly.
  exit /b 1
)

exit /b 0
