Param(
    [string]$PythonVersion = "3.11.9",
    [string]$Architecture = "amd64"
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$distRoot = Join-Path $repoRoot "dist"
$portableRoot = Join-Path $distRoot "FightAI_Portable"
$runtimeRoot = Join-Path $portableRoot "runtime"
$pythonRoot = Join-Path $runtimeRoot "python"
$appRoot = Join-Path $portableRoot "app"
$modelsRoot = Join-Path $portableRoot "models"

if (Test-Path $portableRoot) {
    Remove-Item $portableRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $portableRoot | Out-Null
New-Item -ItemType Directory -Path $runtimeRoot | Out-Null
New-Item -ItemType Directory -Path $appRoot | Out-Null
New-Item -ItemType Directory -Path $modelsRoot | Out-Null

$pythonZipName = "python-$PythonVersion-embed-$Architecture.zip"
$pythonZipPath = Join-Path $distRoot $pythonZipName
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

$requirementsLock = Join-Path $repoRoot "requirements.lock.txt"
if (Test-Path $requirementsLock) {
    $requirementsPayload = Get-Content $requirementsLock | Where-Object { $_ -match '\S' -and $_ -notmatch '^#' }
    if ($requirementsPayload.Count -gt 0) {
        Write-Host "Installing pinned dependencies into runtime..."
        python -m pip install --upgrade pip
        python -m pip install -r $requirementsLock --target (Join-Path $pythonRoot "Lib\site-packages")
    }
}

Write-Host "Copying application code..."
Copy-Item -Path (Join-Path $repoRoot "src\gso_app") -Destination (Join-Path $appRoot "gso_app") -Recurse -Force

Write-Host "Copying models..."
Copy-Item -Path (Join-Path $repoRoot "models\*") -Destination $modelsRoot -Recurse -Force

Write-Host "Building launcher..."
$launcherProject = Join-Path $repoRoot "tools\launcher\FightAI.Launcher\FightAI.Launcher.csproj"
dotnet publish $launcherProject -c Release -r win-x64 -p:PublishSingleFile=true -p:SelfContained=true -p:PublishTrimmed=false -o $portableRoot

Write-Host "Portable build ready at $portableRoot"
