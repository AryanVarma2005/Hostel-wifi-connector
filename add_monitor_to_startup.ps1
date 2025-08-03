# PowerShell script to add WiFi Connection Monitor to Windows startup

# Get the current directory where the script is located
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Create the shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\WiFiConnectionMonitor.lnk")
$Shortcut.TargetPath = "$scriptPath\start_connection_monitor.bat"
$Shortcut.WorkingDirectory = $scriptPath
$Shortcut.Description = "WiFi Connection Monitor"
$Shortcut.Save()

Write-Host "Added WiFi Connection Monitor to Windows startup."
Write-Host "The monitor will now run automatically when you log in to Windows."
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")