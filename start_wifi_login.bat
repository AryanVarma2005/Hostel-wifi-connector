@echo off
echo ===== WiFi Auto Login Enhanced Startup =====
echo.

echo Installing/updating required packages...
pip install -r requirements.txt

echo.
echo Cleaning up any existing ChromeDriver cache...
if exist "%USERPROFILE%\.wdm" (
    rmdir /s /q "%USERPROFILE%\.wdm"
    echo ChromeDriver cache cleaned.
)

echo.
echo Starting WiFi Auto Login with enhanced error handling...
echo The script will automatically recover from errors and restart if needed.
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