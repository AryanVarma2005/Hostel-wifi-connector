# WiFi Auto Login Service Monitor
# This script runs the WiFi login process as a background service with automatic recovery

param(
    [switch]$Install,
    [switch]$Uninstall,
    [switch]$Start,
    [switch]$Stop,
    [switch]$Status
)

$ServiceName = "WiFiAutoLogin"
$ScriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$PythonScript = Join-Path -Path $ScriptPath -ChildPath "wifi_auto_login.py"
$LogFile = Join-Path -Path $ScriptPath -ChildPath "logs\service_monitor.log"

# Create logs directory if it doesn't exist
$LogsDir = Join-Path -Path $ScriptPath -ChildPath "logs"
if (-not (Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
}

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage
    Add-Content -Path $LogFile -Value $logMessage
}

function Test-Service {
    $process = Get-Process -Name "python" -ErrorAction SilentlyContinue | 
               Where-Object { $_.CommandLine -like "*wifi_auto_login.py*" }
    return $process -ne $null
}

function Start-WiFiService {
    Write-Log "Starting WiFi Auto Login service..."
    
    # Clean up ChromeDriver cache first
    $cacheDir = Join-Path -Path $env:USERPROFILE -ChildPath ".wdm"
    if (Test-Path $cacheDir) {
        Write-Log "Cleaning ChromeDriver cache..."
        Remove-Item -Path $cacheDir -Recurse -Force -ErrorAction SilentlyContinue
    }
    
    # Start the Python script in background
    $pythonArgs = @($PythonScript)
    Start-Process -FilePath "python" -ArgumentList $pythonArgs -WindowStyle Hidden
    
    Start-Sleep -Seconds 5
    
    if (Test-Service) {
        Write-Log "WiFi Auto Login service started successfully"
        return $true
    } else {
        Write-Log "Failed to start WiFi Auto Login service"
        return $false
    }
}

function Stop-WiFiService {
    Write-Log "Stopping WiFi Auto Login service..."
    
    $processes = Get-Process -Name "python" -ErrorAction SilentlyContinue | 
                 Where-Object { $_.CommandLine -like "*wifi_auto_login.py*" }
    
    if ($processes) {
        foreach ($process in $processes) {
            Write-Log "Stopping process ID: $($process.Id)"
            Stop-Process -Id $process.Id -Force
        }
        Write-Log "WiFi Auto Login service stopped"
    } else {
        Write-Log "No WiFi Auto Login service found running"
    }
}

function Monitor-WiFiService {
    Write-Log "Starting WiFi Auto Login service monitor..."
    
    while ($true) {
        if (-not (Test-Service)) {
            Write-Log "WiFi Auto Login service not running, starting it..."
            if (-not (Start-WiFiService)) {
                Write-Log "Failed to start service, waiting 60 seconds before retry..."
                Start-Sleep -Seconds 60
            }
        } else {
            Write-Log "WiFi Auto Login service is running normally"
        }
        
        # Check every 5 minutes
        Start-Sleep -Seconds 300
    }
}

# Main execution
if ($Install) {
    Write-Log "Installing WiFi Auto Login service..."
    # Create scheduled task for auto-start
    $taskName = "WiFiAutoLogin"
    $taskAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$PSCommandPath`" -Start"
    $taskTrigger = New-ScheduledTaskTrigger -AtLogOn
    $taskSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    
    Register-ScheduledTask -TaskName $taskName -Action $taskAction -Trigger $taskTrigger -Settings $taskSettings -Force | Out-Null
    Write-Log "WiFi Auto Login service installed successfully"
}

elseif ($Uninstall) {
    Write-Log "Uninstalling WiFi Auto Login service..."
    Stop-WiFiService
    Unregister-ScheduledTask -TaskName "WiFiAutoLogin" -Confirm:$false -ErrorAction SilentlyContinue
    Write-Log "WiFi Auto Login service uninstalled"
}

elseif ($Start) {
    Start-WiFiService
}

elseif ($Stop) {
    Stop-WiFiService
}

elseif ($Status) {
    if (Test-Service) {
        Write-Log "WiFi Auto Login service is running"
        $processes = Get-Process -Name "python" -ErrorAction SilentlyContinue | 
                     Where-Object { $_.CommandLine -like "*wifi_auto_login.py*" }
        foreach ($process in $processes) {
            Write-Log "Process ID: $($process.Id), Started: $($process.StartTime)"
        }
    } else {
        Write-Log "WiFi Auto Login service is not running"
    }
}

else {
    # Default: Start monitoring
    Write-Log "WiFi Auto Login Service Monitor"
    Write-Log "Available commands:"
    Write-Log "  -Install   : Install as Windows service"
    Write-Log "  -Uninstall : Remove Windows service"
    Write-Log "  -Start     : Start the service"
    Write-Log "  -Stop      : Stop the service"
    Write-Log "  -Status    : Check service status"
    Write-Log ""
    Write-Log "Starting service monitor..."
    Monitor-WiFiService
} 