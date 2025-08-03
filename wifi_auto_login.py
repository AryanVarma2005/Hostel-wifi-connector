import time
import subprocess
import requests
import webbrowser
import logging
import configparser
import os
import sys
import shutil
import tempfile
from datetime import datetime

import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging with rotation
import logging.handlers

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging with rotation to prevent large log files
log_handler = logging.handlers.RotatingFileHandler(
    'logs/wifi_login.log',
    maxBytes=1024*1024,  # 1MB
    backupCount=5
)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

class HostelWifiLogin:
    def __init__(self, config_file='config.ini'):
        # Load configuration
        self.config = configparser.ConfigParser()
        
        # Check if config file exists
        if not os.path.exists(config_file):
            logging.error(f"Config file {config_file} not found")
            print(f"Error: Config file {config_file} not found")
            exit(1)
            
        self.config.read(config_file)
        
        # Get login details from config
        self.login_url = self.config.get('WiFiLogin', 'login_url')
        self.username = self.config.get('WiFiLogin', 'username')
        self.password = self.config.get('WiFiLogin', 'password')
        
        # Get element IDs from config
        self.username_field_id = self.config.get('Settings', 'username_field_id')
        self.password_field_id = self.config.get('Settings', 'password_field_id')
        self.login_button_id = self.config.get('Settings', 'login_button_id')
        
        # Get check interval from config
        self.check_interval = self.config.getint('Settings', 'check_interval')
        

        
        self.connected = False
        self.consecutive_failures = 0
        self.max_consecutive_failures = 5
        logging.info("WiFi Auto Login initialized with enhanced error handling")



    def check_internet_connection(self):
        """Check if there is an active internet connection with multiple fallbacks"""
        test_urls = [
            "http://www.google.com",
            "http://www.cloudflare.com",
            "http://www.microsoft.com"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=5, verify=False)
                if response.status_code == 200:
                    return True
            except (requests.ConnectionError, requests.Timeout, requests.RequestException):
                continue
        return False

    def ping_test(self):
        """Alternative method to check connection using ping with multiple targets"""
        ping_targets = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
        
        for target in ping_targets:
            try:
                output = subprocess.check_output(
                    ["ping", "-n", "1", target],
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    timeout=10
                )
                if "Reply from" in output:
                    return True
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                continue
        return False

    def login(self):
        """Attempt to login to the hostel WiFi portal using direct HTTP requests"""
        try:
            logging.info("Attempting to login to WiFi portal")
            
            # Create a session for the requests
            session = requests.Session()
            session.verify = False
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            # Use the specific endpoint that works for this captive portal
            login_endpoint = self.login_url.replace('httpclient.html', 'login.xml')
            
            # Prepare login data based on the working configuration
            login_data = {
                'username': self.username,
                'password': self.password,
                'mode': '191',  # Common mode for captive portals
                'btnSubmit': 'Login'
            }
            
            logging.info(f"Using login endpoint: {login_endpoint}")
            response = session.post(login_endpoint, data=login_data, timeout=10)
            logging.info(f"Login response status: {response.status_code}")
            
            # Check if login was successful
            if response.status_code == 200:
                # Wait a moment for the connection to establish
                time.sleep(2)
                if self.check_internet_connection():
                    logging.info("Login successful - internet connection confirmed")
                    self.consecutive_failures = 0  # Reset failure counter
                    return True
                else:
                    logging.warning("Login response received but internet not available yet")
                    return False
            else:
                logging.error(f"Login failed with status code: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error during login: {e}")
            self.consecutive_failures += 1
            
            # If we have too many consecutive failures, reset counter
            if self.consecutive_failures >= self.max_consecutive_failures:
                logging.warning(f"Too many consecutive failures ({self.consecutive_failures}), resetting counter")
                self.consecutive_failures = 0
            
            return False

    def monitor_connection(self):
        """Continuously monitor the WiFi connection and login when needed with enhanced error handling"""
        logging.info("Starting WiFi connection monitoring with enhanced error handling")
        print(f"WiFi Auto Login started. Checking connection every {self.check_interval} seconds.")
        print(f"Login URL: {self.login_url}")
        print("Press Ctrl+C to stop")
        
        consecutive_errors = 0
        max_consecutive_errors = 10
        
        try:
            while True:
                try:
                    internet_available = self.check_internet_connection() or self.ping_test()
                    
                    if not internet_available and self.connected:
                        logging.info("Internet connection lost")
                        print("Internet connection lost. Attempting to reconnect...")
                        self.connected = False
                    
                    if not internet_available:
                        logging.info("No internet connection detected, attempting to login")
                        print("No internet connection detected, attempting to login...")
                        login_success = self.login()
                        if login_success:
                            self.connected = True
                            print("Successfully logged in to WiFi portal")
                            consecutive_errors = 0  # Reset error counter
                        else:
                            print("Login attempt failed, will retry...")
                    elif not self.connected:
                        logging.info("Internet connection detected")
                        print("Internet connection detected")
                        self.connected = True
                        consecutive_errors = 0  # Reset error counter
                    
                    # Wait before checking again
                    time.sleep(self.check_interval)
                    
                except Exception as e:
                    consecutive_errors += 1
                    logging.error(f"Error in monitoring loop (attempt {consecutive_errors}): {e}")
                    print(f"Error in monitoring: {e}")
                    
                    if consecutive_errors >= max_consecutive_errors:
                        logging.error(f"Too many consecutive errors ({consecutive_errors}), restarting monitoring")
                        print("Too many errors, restarting monitoring...")
                        consecutive_errors = 0
                        time.sleep(30)  # Wait longer before restarting
                    else:
                        time.sleep(10)  # Wait before retrying
                        
        except KeyboardInterrupt:
            print("\nWiFi Auto Login stopped by user")
            logging.info("WiFi Auto Login stopped by user")

def direct_login():
    """Function to directly attempt login without checking connection first"""
    try:
        logging.info("Direct login attempt triggered")
        print("=== Hostel WiFi Direct Login ===\n")
        
        # Check if config file exists
        config_file = 'config.ini'
        if not os.path.exists(config_file):
            print(f"Config file {config_file} not found. Please create it first.")
            print("See README.md for instructions.")
            return False
        
        # Initialize and perform login
        try:
            wifi_login = HostelWifiLogin(config_file)
            login_success = wifi_login.login()
            
            if login_success:
                print("Successfully logged in to WiFi portal")
                return True
            else:
                print("Login attempt failed")
                return False
        except Exception as login_error:
            logging.error(f"Error during direct login attempt: {login_error}")
            print(f"Login error: {login_error}")
            return False
            
    except Exception as e:
        logging.error(f"Unexpected error in direct login: {e}")
        print(f"\nError: {e}")
        print("Check logs/wifi_login.log for details")
        return False

def main():
    """Main function with enhanced error handling"""
    print("=== Hostel WiFi Auto Login (Enhanced Version) ===\n")
    
    # Check if config file exists and create it if it doesn't
    config_file = 'config.ini'
    if not os.path.exists(config_file):
        print(f"Config file {config_file} not found. Please create it first.")
        print("See README.md for instructions.")
        return 1
    
    try:
        # Check if direct login mode is requested
        if len(sys.argv) > 1 and sys.argv[1] == "--direct-login":
            success = direct_login()
            return 0 if success else 1
        else:
            # Initialize and start the WiFi login monitor
            wifi_login = HostelWifiLogin(config_file)
            wifi_login.monitor_connection()
            return 0
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"\nError: {e}")
        print("Check logs/wifi_login.log for details")
        return 1

# Main execution
if __name__ == "__main__":
    exit_code = main()
    if exit_code != 0:
        input("Press Enter to exit...")
    sys.exit(exit_code)