# PowerShell script to add WiFi Auto Login to Windows startup

# Get the current directory where the script is located
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Create the shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\HostelWiFiAutoLogin.lnk")
$Shortcut.TargetPath = "$scriptPath\start_wifi_login.bat"
$Shortcut.WorkingDirectory = $scriptPath
$Shortcut.Description = "Hostel WiFi Auto Login"
$Shortcut.Save()

Write-Host "Added Hostel WiFi Auto Login to Windows startup."
Write-Host "The script will now run automatically when you log in to Windows."
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")