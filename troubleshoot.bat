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
echo Creating logs directory...
if not exist logs (
    mkdir logs
    echo Created logs directory.
) else (
    echo Logs directory exists.
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
echo Testing WiFi login endpoint...
echo Testing connection to the captive portal...
python -c "import requests; import urllib3; urllib3.disable_warnings(); r = requests.get('https://172.16.16.16:8090/httpclient.html', verify=False, timeout=5); print('Captive portal is accessible')" 2>nul
if %ERRORLEVEL% neq 0 (
    echo WARNING: Could not reach the captive portal.
    echo This might be normal if you're not connected to the WiFi network.
) else (
    echo Captive portal is accessible.
)

echo.
echo ===== Troubleshooting Complete =====
echo.
echo If all checks passed, try running:
echo   direct_login.bat
echo.
echo For continuous monitoring, run:
echo   start_wifi_login.bat
echo.
echo Check logs/wifi_login.log for detailed information.
echo.
goto :end

:error
echo.
echo ===== Troubleshooting Failed =====
echo Please fix the errors above and run this script again.
echo.
pause
goto :eof

:end
echo Troubleshooting completed successfully!
pause