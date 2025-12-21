$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$fightAiRoot = Resolve-Path (Join-Path $scriptRoot "..")

$pythonDir = Join-Path $fightAiRoot "runtime/python"
$pythonExe = Join-Path $pythonDir "python.exe"

if (Test-Path $pythonExe) {
    Write-Host "Python runtime already present at $pythonExe"
    exit 0
}

$downloadDir = Join-Path $fightAiRoot "runtime/_download"
$zipName = "python-3.11.9-embed-amd64.zip"
$zipPath = Join-Path $downloadDir $zipName
$downloadUrl = "https://www.python.org/ftp/python/3.11.9/$zipName"

New-Item -ItemType Directory -Force -Path $downloadDir | Out-Null

Write-Host "Downloading $downloadUrl"
Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath

if (Test-Path $pythonDir) {
    Remove-Item -Recurse -Force $pythonDir
}

New-Item -ItemType Directory -Force -Path $pythonDir | Out-Null

Write-Host "Extracting to $pythonDir"
Expand-Archive -Path $zipPath -DestinationPath $pythonDir -Force

if (Test-Path $pythonExe) {
    Write-Host "Python runtime ready at $pythonExe"
    exit 0
}

Write-Error "Python runtime was not found after extraction."
exit 1
