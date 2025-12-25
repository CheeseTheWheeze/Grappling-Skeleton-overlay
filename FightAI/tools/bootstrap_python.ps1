Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$baseDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$runtimeDir = Join-Path $baseDir "runtime\python"
$downloadDir = Join-Path $baseDir "runtime\_download"
$pythonExe = Join-Path $runtimeDir "python.exe"

if (Test-Path $pythonExe) {
    Write-Host "Embedded Python runtime already installed at $pythonExe"
    exit 0
}

New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
New-Item -ItemType Directory -Force -Path $downloadDir | Out-Null

$version = "3.11.9"
$archSuffix = if ([Environment]::Is64BitOperatingSystem) { "amd64" } else { "win32" }
$zipName = "python-$version-embed-$archSuffix.zip"
$zipPath = Join-Path $downloadDir $zipName
$zipUrl = "https://www.python.org/ftp/python/$version/$zipName"

if (-not (Test-Path $zipPath)) {
    Write-Host "Downloading Python $version ($archSuffix) embeddable runtime..."
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath
} else {
    Write-Host "Using cached runtime download at $zipPath"
}

Write-Host "Extracting embedded runtime to $runtimeDir..."
Expand-Archive -Path $zipPath -DestinationPath $runtimeDir -Force

Get-ChildItem -Path $runtimeDir -Filter "python*._pth" | ForEach-Object {
    $pthPath = $_.FullName
    $lines = Get-Content $pthPath

    if ($lines -notcontains "..\\app") {
        $lines += "..\\app"
    }

    if ($lines -notcontains "import site") {
        $lines += "import site"
    }

    Set-Content -Path $pthPath -Value $lines -Encoding ASCII
}

if (-not (Test-Path $pythonExe)) {
    throw "Embedded Python runtime failed to install. Expected $pythonExe"
}

Write-Host "Embedded Python runtime installed successfully."
