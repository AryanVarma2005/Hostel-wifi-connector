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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
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
        
        # Setup Chrome options with better stability
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Run in background
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--ignore-ssl-errors')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-web-security')
        self.chrome_options.add_argument('--allow-running-insecure-content')
        self.chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        self.chrome_options.add_argument('--disable-background-timer-throttling')
        self.chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        self.chrome_options.add_argument('--disable-renderer-backgrounding')
        self.chrome_options.add_argument('--disable-features=TranslateUI')
        self.chrome_options.add_argument('--disable-ipc-flooding-protection')
        
        # Add user agent to avoid detection
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.connected = False
        self.consecutive_failures = 0
        self.max_consecutive_failures = 5
        logging.info("WiFi Auto Login initialized with enhanced error handling")

    def cleanup_chromedriver_cache(self):
        """Clean up corrupted ChromeDriver cache"""
        try:
            cache_dir = os.path.expanduser("~/.wdm")
            if os.path.exists(cache_dir):
                logging.info("Cleaning up ChromeDriver cache...")
                shutil.rmtree(cache_dir)
                logging.info("ChromeDriver cache cleaned")
                return True
        except Exception as e:
            logging.error(f"Error cleaning ChromeDriver cache: {e}")
        return False

    def get_chromedriver_service(self):
        """Get ChromeDriver service with fallback mechanisms"""
        try:
            # First try with webdriver_manager
            driver_path = ChromeDriverManager().install()
            logging.info(f"ChromeDriver installed at: {driver_path}")
            return Service(driver_path)
        except Exception as e:
            logging.error(f"Error with webdriver_manager: {e}")
            
            # Try to clean cache and retry
            if self.cleanup_chromedriver_cache():
                try:
                    driver_path = ChromeDriverManager().install()
                    logging.info(f"ChromeDriver reinstalled at: {driver_path}")
                    return Service(driver_path)
                except Exception as e2:
                    logging.error(f"Error after cache cleanup: {e2}")
            
            # Fallback: try to find ChromeDriver in PATH
            try:
                chrome_path = shutil.which("chromedriver")
                if chrome_path:
                    logging.info(f"Using ChromeDriver from PATH: {chrome_path}")
                    return Service(chrome_path)
            except Exception as e3:
                logging.error(f"Error finding ChromeDriver in PATH: {e3}")
            
            raise Exception("Could not initialize ChromeDriver")

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
        """Attempt to login to the hostel WiFi portal with enhanced error handling"""
        driver = None
        try:
            logging.info("Attempting to login to WiFi portal")
            
            # Get ChromeDriver service with fallback
            service = self.get_chromedriver_service()
            
            # Create driver with retry mechanism
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    driver = webdriver.Chrome(service=service, options=self.chrome_options)
                    break
                except Exception as e:
                    logging.warning(f"Driver creation attempt {attempt + 1} failed: {e}")
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(2)
            
            # Set page load timeout
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            # Navigate to login page
            logging.info(f"Navigating to: {self.login_url}")
            driver.get(self.login_url)
            
            # Wait for the login page to load with multiple fallback strategies
            username_field = None
            wait = WebDriverWait(driver, 15)
            
            try:
                username_field = wait.until(
                    EC.presence_of_element_located((By.ID, self.username_field_id))
                )
            except TimeoutException:
                # Try alternative selectors
                alternative_selectors = [
                    (By.NAME, "username"),
                    (By.NAME, "user"),
                    (By.CSS_SELECTOR, "input[type='text']"),
                    (By.XPATH, "//input[@type='text']")
                ]
                
                for selector_type, selector_value in alternative_selectors:
                    try:
                        username_field = driver.find_element(selector_type, selector_value)
                        logging.info(f"Found username field using {selector_type}: {selector_value}")
                        break
                    except NoSuchElementException:
                        continue
                
                if not username_field:
                    raise Exception("Could not find username field")
            
            # Find password field
            password_field = None
            try:
                password_field = driver.find_element(By.ID, self.password_field_id)
            except NoSuchElementException:
                # Try alternative selectors for password
                alternative_password_selectors = [
                    (By.NAME, "password"),
                    (By.NAME, "pass"),
                    (By.CSS_SELECTOR, "input[type='password']"),
                    (By.XPATH, "//input[@type='password']")
                ]
                
                for selector_type, selector_value in alternative_password_selectors:
                    try:
                        password_field = driver.find_element(selector_type, selector_value)
                        logging.info(f"Found password field using {selector_type}: {selector_value}")
                        break
                    except NoSuchElementException:
                        continue
                
                if not password_field:
                    raise Exception("Could not find password field")
            
            # Clear fields and fill in credentials
            username_field.clear()
            username_field.send_keys(self.username)
            password_field.clear()
            password_field.send_keys(self.password)
            
            # Submit the form with multiple strategies
            login_success = False
            
            # Strategy 1: Try to find and click the button by ID
            try:
                submit_button = driver.find_element(By.ID, self.login_button_id)
                submit_button.click()
                logging.info("Clicked login button by ID")
                login_success = True
            except NoSuchElementException:
                logging.info("Login button not found by ID, trying alternative methods")
                
                # Strategy 2: Try JavaScript function
                try:
                    driver.execute_script("submitRequest()")
                    logging.info("Executed submitRequest() JavaScript function")
                    login_success = True
                except Exception as js_error:
                    logging.info(f"JavaScript execution failed: {js_error}")
                    
                    # Strategy 3: Try to find button by text or other attributes
                    button_selectors = [
                        (By.XPATH, "//button[contains(text(), 'Login')]"),
                        (By.XPATH, "//button[contains(text(), 'Sign In')]"),
                        (By.XPATH, "//input[@type='submit']"),
                        (By.XPATH, "//a[contains(@href, 'javascript:submitRequest()')]"),
                        (By.CSS_SELECTOR, "button[type='submit']"),
                        (By.CSS_SELECTOR, "input[type='submit']")
                    ]
                    
                    for selector_type, selector_value in button_selectors:
                        try:
                            button = driver.find_element(selector_type, selector_value)
                            button.click()
                            logging.info(f"Clicked button using {selector_type}: {selector_value}")
                            login_success = True
                            break
                        except NoSuchElementException:
                            continue
                    
                    # Strategy 4: Try form submission
                    if not login_success:
                        try:
                            form = driver.find_element(By.TAG_NAME, "form")
                            form.submit()
                            logging.info("Submitted form directly")
                            login_success = True
                        except Exception as form_error:
                            logging.error(f"Form submission failed: {form_error}")
            
            if not login_success:
                raise Exception("Could not submit login form")
            
            # Wait for successful login (URL change or redirect)
            try:
                # Wait for URL to change
                original_url = driver.current_url
                wait.until(lambda d: d.current_url != original_url)
                logging.info("Login successful - URL changed")
            except TimeoutException:
                # Check if we're still on the login page
                if "login" in driver.current_url.lower() or "auth" in driver.current_url.lower():
                    raise Exception("Still on login page after submission")
                else:
                    logging.info("Login appears successful - not on login page")
            
            # Test if login actually worked by checking internet
            time.sleep(3)  # Wait a bit for connection to establish
            if self.check_internet_connection():
                logging.info("Internet connection confirmed after login")
                self.consecutive_failures = 0  # Reset failure counter
                return True
            else:
                logging.warning("Login submitted but internet not available")
                return False
            
        except Exception as e:
            logging.error(f"Error during login: {e}")
            self.consecutive_failures += 1
            
            # If we have too many consecutive failures, clean up ChromeDriver cache
            if self.consecutive_failures >= self.max_consecutive_failures:
                logging.warning(f"Too many consecutive failures ({self.consecutive_failures}), cleaning ChromeDriver cache")
                self.cleanup_chromedriver_cache()
                self.consecutive_failures = 0
            
            return False
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception as e:
                    logging.error(f"Error closing driver: {e}")

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