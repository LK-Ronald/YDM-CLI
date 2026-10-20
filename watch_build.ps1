param(
    [string]$Python = "python",
    [int]$DebounceSeconds = 2,
    [int]$PollMilliseconds = 500
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$BuildScript = Join-Path $ProjectRoot "build.py"
$IgnoredDirectories = @(
    ".git",
    "__pycache__",
    "build",
    "dist",
    ".pytest_cache",
    "venv"
)

function Get-SourceSnapshot {
    $snapshot = @{}
    foreach ($file in Get-ChildItem -LiteralPath $ProjectRoot -Recurse -File) {
        if (
            $file.Extension -ne ".py" -and
            $file.Extension -ne ".ps1" -and
            $file.Name -ne "requirements.txt"
        ) {
            continue
        }

        $relativePath = $file.FullName.Substring($ProjectRoot.Length).TrimStart(
            [char[]]@("\", "/")
        )
        $pathParts = $relativePath -split "[\\/]"
        $isIgnored = $false
        foreach ($directory in $IgnoredDirectories) {
            if ($pathParts -contains $directory) {
                $isIgnored = $true
                break
            }
        }
        if ($isIgnored) {
            continue
        }

        $snapshot[$file.FullName] = "{0}:{1}" -f `
            $file.LastWriteTimeUtc.Ticks, $file.Length
    }

    return $snapshot
}

function Test-SnapshotEqual {
    param(
        [hashtable]$First,
        [hashtable]$Second
    )

    if ($First.Count -ne $Second.Count) {
        return $false
    }

    foreach ($path in $First.Keys) {
        if (-not $Second.ContainsKey($path) -or $First[$path] -ne $Second[$path]) {
            return $false
        }
    }

    return $true
}

function Invoke-Build {
    Write-Host "`nCompilando YDM-CLI.exe..."
    & $Python $BuildScript
    if ($LASTEXITCODE -ne 0) {
        Write-Host "La compilación falló (código $LASTEXITCODE). Se seguirá vigilando."
        return $false
    }

    Write-Host "Compilación completada: $(Join-Path $ProjectRoot 'dist\YDM-CLI.exe')"
    return $true
}

$lastBuiltSnapshot = Get-SourceSnapshot
Write-Host "Compilación inicial..."
$null = Invoke-Build

Write-Host "`nVigilando cambios de Python, PowerShell y requirements.txt."
Write-Host "Espera de estabilización: $DebounceSeconds segundos. Ctrl+C para detener."

$lastObservedSnapshot = $lastBuiltSnapshot
$pendingSince = $null

try {
    while ($true) {
        Start-Sleep -Milliseconds $PollMilliseconds
        $currentSnapshot = Get-SourceSnapshot

        if (Test-SnapshotEqual $currentSnapshot $lastBuiltSnapshot) {
            $lastObservedSnapshot = $currentSnapshot
            $pendingSince = $null
            continue
        }

        if (-not (Test-SnapshotEqual $currentSnapshot $lastObservedSnapshot)) {
            $lastObservedSnapshot = $currentSnapshot
            $pendingSince = Get-Date
            continue
        }

        if (((Get-Date) - $pendingSince).TotalSeconds -lt $DebounceSeconds) {
            continue
        }

        $lastBuiltSnapshot = $currentSnapshot
        $null = Invoke-Build
        $pendingSince = $null
    }
}
finally {
    Write-Host "`nVigilancia detenida."
}
