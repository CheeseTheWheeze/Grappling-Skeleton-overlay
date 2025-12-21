param(
    [string]$LogPath = "$env:USERPROFILE\Desktop\GrapplingPipelineCodexLog.txt"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$baseDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$runtimeDir = Join-Path $baseDir "runtime\python"
$downloadDir = Join-Path $baseDir "runtime\_download"
$pythonExe = Join-Path $runtimeDir "python.exe"

if (-not [string]::IsNullOrWhiteSpace($LogPath)) {
    "[{0}] Bootstrap start" -f (Get-Date) | Out-File -FilePath $LogPath -Encoding UTF8
    "Base dir: $baseDir" | Out-File -FilePath $LogPath -Encoding UTF8 -Append
    "Runtime: $pythonExe" | Out-File -FilePath $LogPath -Encoding UTF8 -Append
}

if (Test-Path $pythonExe) {
    Write-Host "Embedded Python runtime already installed at $pythonExe"
    if (-not [string]::IsNullOrWhiteSpace($LogPath)) {
        "Runtime already present." | Out-File -FilePath $LogPath -Encoding UTF8 -Append
    }
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
    if (-not [string]::IsNullOrWhiteSpace($LogPath)) {
        "Downloading runtime from $zipUrl" | Out-File -FilePath $LogPath -Encoding UTF8 -Append
    }
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath
} else {
    Write-Host "Using cached runtime download at $zipPath"
    if (-not [string]::IsNullOrWhiteSpace($LogPath)) {
        "Using cached runtime at $zipPath" | Out-File -FilePath $LogPath -Encoding UTF8 -Append
    }
}

Write-Host "Extracting embedded runtime to $runtimeDir..."
if (-not [string]::IsNullOrWhiteSpace($LogPath)) {
    "Extracting runtime to $runtimeDir" | Out-File -FilePath $LogPath -Encoding UTF8 -Append
}
Expand-Archive -Path $zipPath -DestinationPath $runtimeDir -Force

Get-ChildItem -Path $runtimeDir -Filter "python*._pth" | ForEach-Object {
    $pthPath = $_.FullName
    $lines = Get-Content $pthPath

    $lines = $lines | Where-Object { $_ -ne "..\\app" }

    if ($lines -notcontains "..\\..\\app") {
        $lines += "..\\..\\app"
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
if (-not [string]::IsNullOrWhiteSpace($LogPath)) {
    "Embedded Python runtime installed successfully." | Out-File -FilePath $LogPath -Encoding UTF8 -Append
}
