@echo off
echo ===== WiFi Auto Login Recovery Monitor =====
echo This script will continuously monitor the WiFi login process
echo and automatically restart it if it fails or stops working.
echo.
echo Press Ctrl+C to stop the monitor.
echo.

:monitor_loop
echo [%date% %time%] Starting WiFi Auto Login process...
start /B /WAIT python wifi_auto_login.py
set exit_code=%ERRORLEVEL%

echo [%date% %time%] WiFi Auto Login process exited with code %exit_code%

if %exit_code% neq 0 (
    echo [%date% %time%] Process failed, waiting 60 seconds before restart...
    timeout /t 60 /nobreak > nul
    echo [%date% %time%] Restarting WiFi Auto Login...
) else (
    echo [%date% %time%] Process stopped normally, waiting 30 seconds before restart...
    timeout /t 30 /nobreak > nul
    echo [%date% %time%] Restarting WiFi Auto Login...
)

goto monitor_loop 