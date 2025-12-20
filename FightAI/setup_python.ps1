Param(
    [string]$PythonVersion = "3.11.9",
    [string]$Architecture = "amd64"
)

$ErrorActionPreference = "Stop"

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$runtimeDir = Join-Path $baseDir "runtime"
$pythonRoot = Join-Path $runtimeDir "python"
$pythonExe = Join-Path $pythonRoot "python.exe"

if (Test-Path $pythonExe) {
    Write-Host "Embedded Python already present at $pythonExe"
    return
}

New-Item -ItemType Directory -Path $pythonRoot -Force | Out-Null

$pythonZipName = "python-$PythonVersion-embed-$Architecture.zip"
$pythonZipPath = Join-Path $baseDir $pythonZipName
$pythonUrl = "https://www.python.org/ftp/python/$PythonVersion/$pythonZipName"

if (-not (Test-Path $pythonZipPath)) {
    Write-Host "Downloading Python embeddable runtime $PythonVersion..."
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonZipPath
}

Write-Host "Extracting Python runtime..."
Expand-Archive -Path $pythonZipPath -DestinationPath $pythonRoot -Force

$pthFile = Get-ChildItem -Path $pythonRoot -Filter "python*._pth" | Select-Object -First 1
if (-not $pthFile) {
    throw "Python ._pth file not found in runtime."
}

$versionParts = $PythonVersion.Split('.')
$pyZipTag = "$($versionParts[0])$($versionParts[1])"
$pthContents = @(
    "python$pyZipTag.zip",
    ".",
    "Lib",
    "Lib/site-packages",
    "app",
    "import site"
)
$pthContents | Set-Content -Path $pthFile.FullName -Encoding UTF8

New-Item -ItemType Directory -Path (Join-Path $pythonRoot "Lib\site-packages") -Force | Out-Null

Write-Host "Embedded Python ready."
