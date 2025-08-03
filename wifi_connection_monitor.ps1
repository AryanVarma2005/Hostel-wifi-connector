# PowerShell script to monitor WiFi connections and trigger the login script

# Get the current directory where the script is located
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Function to check if connected to the target WiFi network
function Check-WiFiConnection {
    # Get all network connections
    $networks = Get-NetConnectionProfile
    
    # Check if any network is connected
    if ($networks) {
        Write-Host "Network connection detected. Starting WiFi auto-login..."
        return $true
    }
    
    return $false
}

# Function to start the WiFi auto-login script
function Start-WiFiAutoLogin {
    # For connection monitoring (background process)
    $monitorBatchFilePath = Join-Path -Path $scriptPath -ChildPath "start_wifi_login.bat"
    # For direct login (when connection is detected)
    $directLoginBatchFilePath = Join-Path -Path $scriptPath -ChildPath "direct_login.bat"
    
    # Check if the monitoring process is already running
    $processName = "python"
    $pythonProcesses = Get-Process -Name $processName -ErrorAction SilentlyContinue | 
                      Where-Object { $_.CommandLine -like "*wifi_auto_login.py*" -and $_.CommandLine -notlike "*--direct-login*" }
    
    # First, trigger a direct login attempt
    try {
        Write-Host "Attempting direct login..."
        Start-Process -FilePath $directLoginBatchFilePath -WorkingDirectory $scriptPath -Wait
        Write-Host "Direct login attempt completed."
    } catch {
        Write-Host "Error during direct login: $_"
        Write-Host "Continuing with monitoring..."
    }
    
    # Then, if the monitoring process is not running, start it
    if (-not $pythonProcesses) {
        Write-Host "Starting WiFi auto-login monitoring..."
        try {
            Start-Process -FilePath $monitorBatchFilePath -WorkingDirectory $scriptPath
            Write-Host "WiFi auto-login monitoring started successfully."
        } catch {
            Write-Host "Error starting monitoring: $_"
        }
    } else {
        Write-Host "WiFi auto-login monitoring is already running."
    }
}

# Main monitoring loop
Write-Host "WiFi Connection Monitor started. Press Ctrl+C to stop."

# Initial state
$previousConnectionState = $false

try {
    while ($true) {
        # Check current connection state
        $currentConnectionState = Check-WiFiConnection
        
        # If we just connected to a network
        if ($currentConnectionState -and -not $previousConnectionState) {
            Write-Host "New network connection detected."
            Start-WiFiAutoLogin
        }
        
        # Update previous state
        $previousConnectionState = $currentConnectionState
        
        # Wait before checking again
        Start-Sleep -Seconds 5
    }
} catch {
    Write-Host "Error: $_"
} finally {
    Write-Host "WiFi Connection Monitor stopped."
}