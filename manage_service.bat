@echo off
echo ===== WiFi Auto Login Service Manager =====
echo.

if "%1"=="install" goto :install
if "%1"=="uninstall" goto :uninstall
if "%1"=="start" goto :start
if "%1"=="stop" goto :stop
if "%1"=="status" goto :status
if "%1"=="monitor" goto :monitor

echo Usage: %0 [command]
echo.
echo Commands:
echo   install   - Install WiFi Auto Login as Windows service
echo   uninstall - Remove WiFi Auto Login service
echo   start     - Start the WiFi Auto Login service
echo   stop      - Stop the WiFi Auto Login service
echo   status    - Check service status
echo   monitor   - Start service monitor (auto-restart on failure)
echo.
echo Examples:
echo   %0 install
echo   %0 start
echo   %0 status
echo.
pause
goto :eof

:install
echo Installing WiFi Auto Login service...
powershell -ExecutionPolicy Bypass -File "wifi_service_monitor.ps1" -Install
goto :eof

:uninstall
echo Uninstalling WiFi Auto Login service...
powershell -ExecutionPolicy Bypass -File "wifi_service_monitor.ps1" -Uninstall
goto :eof

:start
echo Starting WiFi Auto Login service...
powershell -ExecutionPolicy Bypass -File "wifi_service_monitor.ps1" -Start
goto :eof

:stop
echo Stopping WiFi Auto Login service...
powershell -ExecutionPolicy Bypass -File "wifi_service_monitor.ps1" -Stop
goto :eof

:status
echo Checking WiFi Auto Login service status...
powershell -ExecutionPolicy Bypass -File "wifi_service_monitor.ps1" -Status
goto :eof

:monitor
echo Starting WiFi Auto Login service monitor...
powershell -ExecutionPolicy Bypass -File "wifi_service_monitor.ps1"
goto :eof 