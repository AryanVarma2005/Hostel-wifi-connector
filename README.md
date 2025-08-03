# Hostel WiFi Auto Login (Enhanced Version)

This tool automatically detects when your WiFi connection is lost and handles the sign-in process for your hostel WiFi portal. It can also automatically trigger when you connect to your WiFi network, even when offline, by immediately filling in your login details.

## 🚀 New Features in Enhanced Version

- **Automatic Recovery**: Script automatically restarts if it crashes or stops working
- **ChromeDriver Cache Management**: Automatically cleans corrupted ChromeDriver cache
- **Multiple Fallback Strategies**: Uses multiple methods to find and interact with login elements
- **Enhanced Error Handling**: Comprehensive error recovery and logging
- **Service Mode**: Run as a Windows service with automatic monitoring
- **Rotating Logs**: Prevents log files from growing too large
- **Multiple Connection Tests**: Tests multiple servers to verify internet connectivity
- **Automatic Restart**: Built-in restart mechanism for long-term reliability

## Features

- Monitors internet connectivity continuously
- Automatically detects when connection is lost
- Automatically logs into the hostel WiFi portal
- Can trigger automatically when connecting to WiFi networks
- Works offline - immediately fills login details when a new connection is detected
- Runs in the background with minimal resource usage
- Logs all activities for troubleshooting
- **NEW**: Automatic recovery and restart on failure
- **NEW**: ChromeDriver cache cleanup and management
- **NEW**: Multiple fallback strategies for login elements
- **NEW**: Service mode for Windows startup

## Requirements for installation
- Python 3.6 or higher
- Chrome browser installed
- ChromeDriver (will be automatically installed by Selenium)

## Setup Instructions

1. Update your login credentials using one of these methods:

   **Option A: Use the credential update tool (Recommended)**
   
   Run the `update_credentials.bat` file and follow the prompts to enter your username and password.
   
   **Option B: Edit the config file manually**
   
   Edit the `config.ini` file and update the following settings with your information:
   ```ini
   [WiFiLogin]
   # College WiFi login page URL (already configured)
   login_url = https://172.16.16.16:8090/httpclient.html
   
   # Replace with your login credentials
   username = your_username
   password = your_password
   
   [Settings]
   # Check interval in seconds (how often to check if WiFi is connected)
   check_interval = 30
   
   # Element IDs on the login page (already configured for your college WiFi)
   username_field_id = username
   password_field_id = password
   login_button_id = loginbutton
   ```

2. The element IDs (`username_field_id`, `password_field_id`, and `login_button_id`) should match the actual HTML element IDs on your hostel's login page. You may need to inspect the login page to find the correct IDs.

   **Note for College WiFi (172.16.16.16:8090)**: The script has been configured for this specific login page. The login button uses a JavaScript function called `submitRequest()` which the script will automatically handle.

## Usage

### Quick Start (Recommended)

1. **Run the enhanced startup script**:
   ```
   start_wifi_login.bat
   ```
   This will install dependencies, clean ChromeDriver cache, and start the script with automatic recovery.

### Service Mode (Best for Long-term Use)

1. **Install as Windows service**:
   ```
   manage_service.bat install
   ```

2. **Start the service**:
   ```
   manage_service.bat start
   ```

3. **Check service status**:
   ```
   manage_service.bat status
   ```

4. **Stop the service**:
   ```
   manage_service.bat stop
   ```

5. **Uninstall the service**:
   ```
   manage_service.bat uninstall
   ```

### Manual Start

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the script:
   ```
   python wifi_auto_login.py
   ```

### Direct Login

If you want to manually trigger a login attempt without checking internet connectivity first:

```
python wifi_auto_login.py --direct-login
```

## Run on Startup (Windows)

### Method 1: Service Mode (Recommended)

1. Install the service:
   ```
   manage_service.bat install
   ```

2. The WiFi Auto Login will now run automatically when you log in to your computer and restart automatically if it fails.

### Method 2: Automatic Recovery Monitor

1. Double-click the `auto_recovery_monitor.bat` file
2. This will start a monitor that continuously runs the WiFi login and restarts it if it fails

### Method 3: Standard Startup

1. Right-click on `add_to_startup.ps1` and select "Run with PowerShell"
2. The script will create a shortcut in your Windows startup folder
3. The WiFi Auto Login will now run automatically when you log in to your computer

### Method 4: WiFi Connection Monitoring

To automatically trigger the login process when you connect to WiFi:

1. Double-click the `add_monitor_to_startup.bat` file
2. This will add the WiFi Connection Monitor to your Windows startup
3. The monitor will detect when you connect to WiFi networks and automatically trigger the login process

## Troubleshooting

### Automatic Troubleshooting

Run the enhanced troubleshooting script:

```
troubleshoot.bat
```

This script will check for:
- Required files (wifi_auto_login.py, config.ini, requirements.txt)
- Python installation
- Required Python packages
- Chrome browser installation
- Internet connection
- ChromeDriver cache cleanup
- Common configuration errors

### Manual Troubleshooting

Check the `logs/wifi_login.log` file for error messages and debugging information.

### Common Issues and Solutions

1. **ChromeDriver errors**: The enhanced version automatically cleans ChromeDriver cache and uses multiple fallback strategies. If issues persist, run `troubleshoot.bat`.

2. **Script can't find login elements**: The enhanced version uses multiple strategies to find login elements. If it still fails, you may need to update the element IDs in the config.ini file.

3. **Script crashes after long periods**: The enhanced version includes automatic recovery and restart mechanisms. Use service mode for the most reliable long-term operation.

4. **Login page not loading**: Verify that the login URL in config.ini is correct and accessible.

5. **Script doesn't detect disconnection**: The script checks connectivity based on the interval set in config.ini. You can adjust this value if needed.

### Recovery Options

If the script stops working:

1. **Quick fix**: Run `start_wifi_login.bat` - this will clean cache and restart
2. **Service restart**: Run `manage_service.bat restart`
3. **Full reset**: Run `troubleshoot.bat` then `start_wifi_login.bat`

## Advanced Configuration

### Configuration Options

All customization options are available in the `config.ini` file:

- **check_interval**: Change how often (in seconds) the script checks for connectivity
- **username_field_id**, **password_field_id**, **login_button_id**: Adjust these if your hostel's login page uses different HTML element IDs

### Service Configuration

The service monitor checks every 5 minutes if the WiFi login process is running and restarts it if needed. You can modify this interval in `wifi_service_monitor.ps1`.

### Log Management

- Logs are stored in the `logs/` directory
- Log files are automatically rotated when they reach 1MB
- Up to 5 backup log files are kept
- Service monitor logs are in `logs/service_monitor.log`

## Customization

### Advanced Customization

For more advanced customization, you can modify the Python script directly:

- To run the browser visibly (not in headless mode), edit `wifi_auto_login.py` and remove or comment out the line `self.chrome_options.add_argument("--headless")`
- To add additional browser options, modify the Chrome options in the `__init__` method
- To change how the script detects internet connectivity, modify the `check_internet_connection` and `ping_test` methods
- To adjust recovery behavior, modify the `max_consecutive_failures` and `max_consecutive_errors` variables

## File Structure

```
Hostel/
├── wifi_auto_login.py              # Main WiFi login script (enhanced)
├── config.ini                      # Configuration file
├── requirements.txt                # Python dependencies
├── start_wifi_login.bat           # Enhanced startup script
├── manage_service.bat             # Service management script
├── wifi_service_monitor.ps1       # PowerShell service monitor
├── auto_recovery_monitor.bat      # Automatic recovery monitor
├── troubleshoot.bat               # Enhanced troubleshooting script
├── logs/                          # Log directory (auto-created)
│   ├── wifi_login.log             # Main application logs
│   └── service_monitor.log        # Service monitor logs
└── [other existing files...]
```

## Support

If you encounter issues:

1. Run `troubleshoot.bat` first
2. Check the logs in the `logs/` directory
3. Try the service mode: `manage_service.bat install` then `manage_service.bat start`
4. If problems persist, the enhanced version includes comprehensive error logging to help identify the issue