@echo off
echo ===== WiFi Auto Login Troubleshooter =====
echo.

echo Checking for required files...

if not exist wifi_auto_login.py (
    echo ERROR: wifi_auto_login.py not found!
    echo This file is required for the WiFi Auto Login to work.
    goto :error
) else (
    echo FOUND: wifi_auto_login.py
)

if not exist config.ini (
    echo WARNING: config.ini not found!
    echo This file is required for storing your login credentials.
    echo Creating a template config.ini file...
    echo [WiFiLogin]> config.ini
    echo login_url = https://172.16.16.16:8090/httpclient.html>> config.ini
    echo username = >> config.ini
    echo password = >> config.ini
    echo [Settings]>> config.ini
    echo check_interval = 30>> config.ini
    echo username_field_id = username>> config.ini
    echo password_field_id = password>> config.ini
    echo login_button_id = loginbutton>> config.ini
    echo Created config.ini - Please update with your credentials using update_credentials.bat
) else (
    echo FOUND: config.ini
)

echo.
echo Checking Python installation...
python --version 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.6 or higher from https://www.python.org/downloads/
    goto :error
) else (
    echo Python is installed.
)

echo.
echo Checking required Python packages...
echo Installing/updating required packages...
pip install -r requirements.txt

echo.
echo Checking Chrome installation...
where chrome 2>nul
if %ERRORLEVEL% neq 0 (
    echo WARNING: Chrome not found in PATH.
    echo Please make sure Google Chrome is installed.
) else (
    echo Chrome is installed.
)

echo.
echo Checking internet connection...
ping -n 1 8.8.8.8 >nul
if %ERRORLEVEL% neq 0 (
    echo WARNING: No internet connection detected.
    echo This is normal if you're not connected to WiFi or need to log in.
) else (
    echo Internet connection is working.
)

echo.
echo Checking WiFi connection monitor...
if not exist wifi_connection_monitor.ps1 (
    echo WARNING: wifi_connection_monitor.ps1 not found!
    echo This file is required for automatic WiFi connection detection.
) else (
    echo FOUND: wifi_connection_monitor.ps1
)

echo.
echo Troubleshooting complete!
echo.
echo If you're still having issues, please check the wifi_login.log file for error messages.
echo.
echo Press any key to exit...
pause > nul
goto :eof

:error
echo.
echo Troubleshooting failed! Please fix the errors above before continuing.
echo.
echo Press any key to exit...
pause > nul