# Hostel WiFi Auto Login

A simple and reliable WiFi auto-login script for hostel captive portals. This script automatically detects when you're connected to the WiFi network and logs you in using your credentials.

## Features

- ✅ **Automatic Login**: Detects when WiFi connection is available and logs in automatically
- ✅ **Continuous Monitoring**: Monitors your connection and re-logs in when needed
- ✅ **No Browser Dependencies**: Uses direct HTTP requests (no ChromeDriver or Selenium needed)
- ✅ **Error Recovery**: Automatically restarts if it encounters errors
- ✅ **Windows Startup**: Can be configured to start automatically on boot
- ✅ **Logging**: Detailed logs for troubleshooting

## Quick Start

### 1. Setup

1. **Install Python** (3.6 or higher) from [python.org](https://www.python.org/downloads/)
2. **Download this project** to your computer
3. **Configure your credentials** by running:
   ```bash
   update_credentials.bat
   ```

### 2. Test the Login

Run a one-time login test:
```bash
direct_login.bat
```

### 3. Start Continuous Monitoring

For automatic monitoring and login:
```bash
start_wifi_login.bat
```

## Configuration

The script uses `config.ini` for configuration. You can edit it manually or use the provided tools:

### Manual Configuration
1. Copy `config_template.ini` to `config.ini`
2. Edit `config.ini`:
```ini
[WiFiLogin]
login_url = https://172.16.16.16:8090/httpclient.html
username = YOUR_USERNAME
password = YOUR_PASSWORD

[Settings]
check_interval = 30
username_field_id = username
password_field_id = password
login_button_id = loginbutton
```

### Using the Update Tool
```bash
update_credentials.bat
```

**Note**: The `config.ini` file with your credentials is protected by `.gitignore` and will not be uploaded to the repository. Use `config_template.ini` as a starting point.

## Usage

### Direct Login (One-time)
```bash
python wifi_auto_login.py --direct-login
```

### Continuous Monitoring
```bash
python wifi_auto_login.py
```

### Using Batch Files
- **`direct_login.bat`** - One-time login test
- **`start_wifi_login.bat`** - Start continuous monitoring with auto-restart

## Windows Startup

To make the script start automatically when you log in to Windows:

```bash
add_to_startup.ps1
```

This will add the WiFi auto-login to your Windows startup folder.

## Troubleshooting

### Run the Troubleshooter
```bash
troubleshoot.bat
```

This will check:
- Python installation
- Required packages
- Configuration files
- Internet connection
- Captive portal accessibility

### Check Logs
Logs are stored in the `logs/` directory:
- `logs/wifi_login.log` - Main application logs

### Common Issues

1. **"Config file not found"**
   - Run `update_credentials.bat` to create the config file

2. **"Python not found"**
   - Install Python from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

3. **"Login failed"**
   - Check your credentials in `config.ini`
   - Verify you're connected to the WiFi network
   - Check the logs for detailed error messages

4. **"No internet connection"**
   - This is normal if you're not logged in to the WiFi
   - The script will automatically attempt to log in

## How It Works

The script works by:

1. **Monitoring Connection**: Checks if internet is available every 30 seconds
2. **Detecting Captive Portal**: When no internet is available, it attempts to log in
3. **Direct HTTP Login**: Sends login credentials directly to the captive portal endpoint
4. **Verification**: Confirms successful login by checking internet connectivity
5. **Auto-Recovery**: Restarts automatically if it encounters errors

## Technical Details

- **Login Endpoint**: `https://172.16.16.16:8090/login.xml`
- **Method**: HTTP POST with form data
- **Dependencies**: `requests`, `configparser`, `urllib3`
- **Compatibility**: Windows 10/11 with Python 3.6+

## Files

### Core Files
- `wifi_auto_login.py` - Main application script
- `config.ini` - Configuration file with credentials
- `requirements.txt` - Python dependencies

### Batch Files
- `direct_login.bat` - One-time login test
- `start_wifi_login.bat` - Start continuous monitoring
- `update_credentials.bat` - Update login credentials
- `troubleshoot.bat` - Troubleshooting tool

### PowerShell Scripts
- `add_to_startup.ps1` - Add to Windows startup
- `update_credentials.py` - Credential update utility

### Directories
- `logs/` - Application logs

## Development

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
python wifi_auto_login.py --direct-login
```

## License

This project is provided as-is for educational and personal use.

## Support

If you encounter issues:
1. Run `troubleshoot.bat`
2. Check the logs in `logs/wifi_login.log`
3. Verify your credentials in `config.ini`
4. Make sure you're connected to the WiFi network