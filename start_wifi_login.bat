@echo off
echo ===== WiFi Auto Login Startup =====
echo.

echo Installing/updating required packages...
pip install -r requirements.txt

echo.
echo Starting WiFi Auto Login...
echo The script will automatically monitor your WiFi connection and login when needed.
echo.

:start_loop
python wifi_auto_login.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo Script exited with error code %ERRORLEVEL%
    echo Waiting 30 seconds before restarting...
    timeout /t 30 /nobreak > nul
    echo Restarting WiFi Auto Login...
    goto start_loop
)

echo.
echo WiFi Auto Login stopped normally.
pause