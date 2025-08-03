import time
import subprocess
import requests
import webbrowser
import logging
import configparser
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    filename='wifi_login.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
        
        # Setup Chrome options
        self.chrome_options = Options()
        # Run in background (comment out for debugging)
        self.chrome_options.add_argument("--headless")  # Run in background
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        # Add option to ignore SSL certificate errors (for https URLs)
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--ignore-ssl-errors')
        # Additional options for stability
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-gpu')
        self.connected = False
        logging.info("WiFi Auto Login initialized")

    def check_internet_connection(self):
        """Check if there is an active internet connection"""
        try:
            # Try to connect to Google's DNS server
            response = requests.get("http://www.google.com", timeout=5)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            pass
        except requests.Timeout:
            pass
        return False

    def ping_test(self):
        """Alternative method to check connection using ping"""
        try:
            # Ping Google's DNS server
            output = subprocess.check_output(
                ["ping", "-n", "1", "8.8.8.8"],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            if "Reply from 8.8.8.8" in output:
                return True
            return False
        except subprocess.CalledProcessError:
            return False

    def login(self):
        """Attempt to login to the hostel WiFi portal"""
        try:
            logging.info("Attempting to login to WiFi portal")
            # Use webdriver_manager to handle ChromeDriver installation
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=self.chrome_options
            )
            driver.get(self.login_url)
            
            # Wait for the login page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, self.username_field_id))
            )
            
            # Fill in the login form
            username_field = driver.find_element(By.ID, self.username_field_id)
            password_field = driver.find_element(By.ID, self.password_field_id)
            
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            
            # Submit the form
            try:
                # First try to find the button by ID
                submit_button = driver.find_element(By.ID, self.login_button_id)
                submit_button.click()
            except NoSuchElementException:
                # If button not found by ID, try to find by JavaScript function
                logging.info("Login button not found by ID, trying JavaScript approach")
                try:
                    # Try to execute the submitRequest() JavaScript function
                    driver.execute_script("submitRequest()")
                    logging.info("Executed submitRequest() JavaScript function")
                except Exception as js_error:
                    logging.error(f"JavaScript execution error: {js_error}")
                    # As a last resort, try to find and click the anchor tag
                    submit_link = driver.find_element(By.XPATH, "//a[contains(@href, 'javascript:submitRequest()')]")
                    submit_link.click()
                    logging.info("Clicked on submit link")
            
            # Wait for successful login
            WebDriverWait(driver, 10).until(
                EC.url_changes(self.login_url)
            )
            
            logging.info("Login successful")
            driver.quit()
            return True
            
        except TimeoutException:
            logging.error("Timeout while trying to login")
        except NoSuchElementException as e:
            logging.error(f"Element not found: {e}")
        except Exception as e:
            logging.error(f"Error during login: {e}")
        
        try:
            driver.quit()
        except:
            pass
            
        return False

    def monitor_connection(self):
        """Continuously monitor the WiFi connection and login when needed"""
        logging.info("Starting WiFi connection monitoring")
        print(f"WiFi Auto Login started. Checking connection every {self.check_interval} seconds.")
        print(f"Login URL: {self.login_url}")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                internet_available = self.check_internet_connection() or self.ping_test()
                
                if not internet_available and self.connected:
                    logging.info("Internet connection lost")
                    print("Internet connection lost. Attempting to reconnect...")
                    self.connected = False
                
                if not internet_available:
                    logging.info("No internet connection detected, attempting to login")
                    login_success = self.login()
                    if login_success:
                        self.connected = True
                        print("Successfully logged in to WiFi portal")
                elif not self.connected:
                    logging.info("Internet connection detected")
                    print("Internet connection detected")
                    self.connected = True
                    
                # Wait before checking again
                time.sleep(self.check_interval)
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
                print("Login attempt failed, but will continue monitoring")
                return False
        except Exception as login_error:
            logging.error(f"Error during direct login attempt: {login_error}")
            print(f"Login error: {login_error}")
            print("Will continue monitoring for connection changes")
            return False
            
    except Exception as e:
        logging.error(f"Unexpected error in direct login: {e}")
        print(f"\nError: {e}")
        print("Check wifi_login.log for details")
        return False

# Main execution
if __name__ == "__main__":
    # Check for command line arguments
    import sys
    
    print("=== Hostel WiFi Auto Login ===\n")
    
    # Check if config file exists and create it if it doesn't
    config_file = 'config.ini'
    if not os.path.exists(config_file):
        print(f"Config file {config_file} not found. Please create it first.")
        print("See README.md for instructions.")
        exit(1)
    
    try:
        # Check if direct login mode is requested
        if len(sys.argv) > 1 and sys.argv[1] == "--direct-login":
            direct_login()
        else:
            # Initialize and start the WiFi login monitor
            wifi_login = HostelWifiLogin(config_file)
            wifi_login.monitor_connection()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"\nError: {e}")
        print("Check wifi_login.log for details")
        input("Press Enter to exit...")