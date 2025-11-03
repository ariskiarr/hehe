param(
    [Parameter(Mandatory=$true)] [string] $ScriptPath,
    [string] $TaskName = "GitAutoCommitPush",
    [string] $Time = "09:00"
)

# Creates a scheduled task that runs the given python script daily at the specified time
if (-not (Test-Path $ScriptPath)) {
    Write-Error "Script not found: $ScriptPath"
    exit 1
}

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -Command \"python \"`\"$ScriptPath`\"\""
$trigger = New-ScheduledTaskTrigger -Daily -At $Time

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -RunLevel LeastPrivilege -Force

Write-Host "Scheduled task '$TaskName' created to run $ScriptPath daily at $Time."
