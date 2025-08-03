# Hostel WiFi Auto Login 

This tool automatically detects when your WiFi connection is lost and handles the sign-in process for your hostel WiFi portal. It can also automatically trigger when you connect to your WiFi network, even when offline, by immediately filling in your login details.

## Features

- Monitors internet connectivity continuously
- Automatically detects when connection is lost
- Automatically logs into the hostel WiFi portal
- Can trigger automatically when connecting to WiFi networks
- Works offline - immediately fills login details when a new connection is detected
- Runs in the background with minimal resource usage
- Logs all activities for troubleshooting

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

### Windows

1. Double-click the `start_wifi_login.bat` file to install dependencies and start the script.

### Manual Start

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the script:
   ```
   python wifi_auto_login.py
   ```

## Run on Startup (Windows)

### Automatic Method (Standard Login Monitor)

1. Right-click on `add_to_startup.ps1` and select "Run with PowerShell"
2. The script will create a shortcut in your Windows startup folder
3. The WiFi Auto Login will now run automatically when you log in to your computer

### Automatic WiFi Connection Monitoring

To automatically trigger the login process when you connect to WiFi:

1. Double-click the `add_monitor_to_startup.bat` file
2. This will add the WiFi Connection Monitor to your Windows startup
3. The monitor will detect when you connect to WiFi networks and automatically trigger the login process
4. When a new connection is detected, it will immediately attempt to log in without waiting to check internet connectivity

You can also manually start the connection monitor by running `start_connection_monitor.bat`

### Direct Login

If you want to manually trigger a login attempt without checking internet connectivity first:

1. Double-click the `direct_login.bat` file
2. This will immediately attempt to log in to the WiFi portal

### Manual Method

1. Press `Win + R` and type `shell:startup` to open the Startup folder
2. Create a shortcut to the `start_wifi_login.bat` file in this folder
3. The script will now run automatically when you log in to your computer

## Troubleshooting

### Automatic Troubleshooting

Run the `troubleshoot.bat` script to automatically check for common issues:

```
troubleshoot.bat
```

This script will check for:
- Required files (wifi_auto_login.py, config.ini, requirements.txt)
- Python installation
- Required Python packages
- Chrome browser installation
- Internet connection
- Common configuration errors

### Manual Troubleshooting

Check the `wifi_login.log` file for error messages and debugging information.

Common issues:

1. **Script can't find login elements**: You may need to update the element IDs in the config.ini file to match your hostel's login page. For the college WiFi portal (172.16.16.16:8090), the script has been enhanced to try multiple methods to submit the login form, including executing the JavaScript function directly.
2. **Chrome crashes**: Make sure you have the latest version of Chrome installed.
3. **Script doesn't detect disconnection**: The script checks connectivity based on the interval set in config.ini. You can adjust this value if needed.
4. **Login page not loading**: Verify that the login URL in config.ini is correct and accessible.
5. **Script crashes on startup**: Make sure all required packages are installed by running `pip install -r requirements.txt`.

## Customization

### Configuration Options

All customization options are available in the `config.ini` file:

- **check_interval**: Change how often (in seconds) the script checks for connectivity
- **username_field_id**, **password_field_id**, **login_button_id**: Adjust these if your hostel's login page uses different HTML element IDs

### Advanced Customization

For more advanced customization, you can modify the Python script directly:

- To run the browser visibly (not in headless mode), edit `wifi_auto_login.py` and remove or comment out the line `self.chrome_options.add_argument("--headless")`
- To add additional browser options, modify the Chrome options in the `__init__` method
- To change how the script detects internet connectivity, modify the `check_internet_connection` and `ping_test` methods