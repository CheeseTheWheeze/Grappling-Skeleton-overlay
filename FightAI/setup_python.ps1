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
if ($Architecture -eq "amd64") {
    $installerName = "python-$PythonVersion-amd64.exe"
} else {
    $installerName = "python-$PythonVersion.exe"
}
$installerPath = Join-Path $baseDir $installerName

if (-not (Test-Path $pythonZipPath)) {
    throw "Missing bundled runtime: $pythonZipName. Place it next to FightAI.cmd."
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

function Install-TkinterRuntime {
    param(
        [string]$LayoutRoot,
        [string]$RuntimeRoot
    )

    $tclTarget = Join-Path $RuntimeRoot "tcl"
    if (Test-Path $tclTarget) {
        return
    }

    if (-not (Test-Path $installerPath)) {
        throw "Missing bundled installer: $installerName. Place it next to FightAI.cmd."
    }

    Write-Host "Extracting Tkinter runtime from installer..."
    $layoutArgs = "/layout `"$LayoutRoot`" /quiet"
    Start-Process -Wait -FilePath $installerPath -ArgumentList $layoutArgs

    $tclMsi = Get-ChildItem -Path $LayoutRoot -Filter "tcltk*.msi" -Recurse | Select-Object -First 1
    if (-not $tclMsi) {
        throw "Tkinter MSI not found in layout."
    }

    $tclExtract = Join-Path $LayoutRoot "tcltk"
    Start-Process -Wait -FilePath "msiexec.exe" -ArgumentList "/a `"$($tclMsi.FullName)`" /qn TARGETDIR=`"$tclExtract`""

    $tclSource = Join-Path $tclExtract "tcl"
    if (Test-Path $tclSource) {
        Copy-Item -Path $tclSource -Destination $RuntimeRoot -Recurse -Force
    }

    $tkinterFiles = @(
        "DLLs\\_tkinter.pyd",
        "DLLs\\tcl86t.dll",
        "DLLs\\tk86t.dll"
    )
    foreach ($file in $tkinterFiles) {
        $dest = Join-Path $RuntimeRoot $file
        if (Test-Path $dest) {
            continue
        }
        $source = Get-ChildItem -Path $tclExtract -Filter ([System.IO.Path]::GetFileName($file)) -Recurse | Select-Object -First 1
        if ($source) {
            $destDir = Split-Path -Parent $dest
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            Copy-Item -Path $source.FullName -Destination $dest -Force
        }
    }
}

Install-TkinterRuntime -LayoutRoot (Join-Path $baseDir "python-layout") -RuntimeRoot $pythonRoot

Write-Host "Embedded Python ready."
