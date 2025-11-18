param(
    [Parameter(Mandatory=$true)][string] $ScriptPath,
    [string] $Repo = ".",
    [string] $Branch = "main",
    [int] $Count = 7,
    [int] $DelaySeconds = 10
)

if (-not (Test-Path $ScriptPath)) {
    Write-Error "Script not found: $ScriptPath"
    exit 1
}

Write-Host "Running commit bot $Count times against repo: $Repo (branch: $Branch)"
for ($i = 1; $i -le $Count; $i++) {
    $now = Get-Date -Format "u"
    Write-Host "Run $i/$Count - $now"

    # Execute python script and stream output
    & python $ScriptPath --repo $Repo --branch $Branch 2>&1 | ForEach-Object { Write-Host $_ }

    if ($i -lt $Count) {
        Start-Sleep -Seconds $DelaySeconds
    }
}

Write-Host "All runs complete."
