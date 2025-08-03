#!/usr/bin/env python3
"""
Test script to verify WiFi Auto Login setup
"""

import os
import sys
import configparser
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_python_imports():
    """Test if all required Python packages are installed"""
    print("Testing Python imports...")
    
    try:
        import requests
        print("✓ requests module imported successfully")
    except ImportError:
        print("✗ requests module not found")
        return False
    
    try:
        import selenium
        print("✓ selenium module imported successfully")
    except ImportError:
        print("✗ selenium module not found")
        return False
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("✓ webdriver-manager module imported successfully")
    except ImportError:
        print("✗ webdriver-manager module not found")
        return False
    
    try:
        import configparser
        print("✓ configparser module imported successfully")
    except ImportError:
        print("✗ configparser module not found")
        return False
    
    return True

def test_config_file():
    """Test if config.ini exists and is valid"""
    print("\nTesting configuration file...")
    
    if not os.path.exists('config.ini'):
        print("✗ config.ini file not found")
        return False
    
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        required_sections = ['WiFiLogin', 'Settings']
        for section in required_sections:
            if section not in config.sections():
                print(f"✗ Missing section: {section}")
                return False
        
        required_keys = {
            'WiFiLogin': ['login_url', 'username', 'password'],
            'Settings': ['check_interval', 'username_field_id', 'password_field_id', 'login_button_id']
        }
        
        for section, keys in required_keys.items():
            for key in keys:
                if not config.has_option(section, key):
                    print(f"✗ Missing key: {section}.{key}")
                    return False
        
        print("✓ config.ini file is valid")
        return True
        
    except Exception as e:
        print(f"✗ Error reading config.ini: {e}")
        return False

def test_chrome_installation():
    """Test if Chrome is installed"""
    print("\nTesting Chrome installation...")
    
    try:
        # Try to find Chrome in common locations
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        ]
        
        chrome_found = False
        for path in chrome_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                print(f"✓ Chrome found at: {expanded_path}")
                chrome_found = True
                break
        
        if not chrome_found:
            # Try using where command
            result = subprocess.run(['where', 'chrome'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Chrome found in PATH: {result.stdout.strip()}")
                chrome_found = True
        
        if not chrome_found:
            print("✗ Chrome not found. Please install Google Chrome.")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error checking Chrome installation: {e}")
        return False

def test_chromedriver():
    """Test ChromeDriver installation"""
    print("\nTesting ChromeDriver installation...")
    
    try:
        # Test webdriver-manager
        driver_path = ChromeDriverManager().install()
        print(f"✓ ChromeDriver installed at: {driver_path}")
        
        # Test creating a Chrome service
        service = Service(driver_path)
        print("✓ ChromeDriver service created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ ChromeDriver test failed: {e}")
        return False

def test_internet_connection():
    """Test internet connectivity"""
    print("\nTesting internet connection...")
    
    test_urls = [
        "http://www.google.com",
        "http://www.cloudflare.com",
        "http://www.microsoft.com"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5, verify=False)
            if response.status_code == 200:
                print(f"✓ Internet connection working (tested with {url})")
                return True
        except Exception:
            continue
    
    print("✗ No internet connection detected")
    return False

def test_wifi_login_page():
    """Test if WiFi login page is accessible"""
    print("\nTesting WiFi login page accessibility...")
    
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        login_url = config.get('WiFiLogin', 'login_url')
        
        # Test with requests first
        try:
            response = requests.get(login_url, timeout=10, verify=False)
            if response.status_code == 200:
                print(f"✓ WiFi login page accessible: {login_url}")
                return True
        except Exception as e:
            print(f"⚠ Could not access login page with requests: {e}")
            print("This might be normal if the page requires JavaScript")
        
        # Try with Selenium
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            driver.set_page_load_timeout(30)
            driver.get(login_url)
            
            print(f"✓ WiFi login page loaded successfully with Selenium: {login_url}")
            print(f"  Page title: {driver.title}")
            
            driver.quit()
            return True
            
        except Exception as e:
            print(f"✗ Could not load login page with Selenium: {e}")
            return False
        
    except Exception as e:
        print(f"✗ Error testing login page: {e}")
        return False

def main():
    """Run all tests"""
    print("=== WiFi Auto Login Setup Test ===\n")
    
    tests = [
        test_python_imports,
        test_config_file,
        test_chrome_installation,
        test_chromedriver,
        test_internet_connection,
        test_wifi_login_page
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Your WiFi Auto Login setup is ready.")
        print("\nYou can now run:")
        print("  start_wifi_login.bat          # Quick start")
        print("  manage_service.bat install    # Install as service")
        print("  python wifi_auto_login.py     # Manual start")
    else:
        print("✗ Some tests failed. Please fix the issues above before using WiFi Auto Login.")
        print("\nTry running:")
        print("  troubleshoot.bat              # Automatic troubleshooting")
        print("  pip install -r requirements.txt  # Install dependencies")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    if not success:
        input("\nPress Enter to exit...")
    sys.exit(0 if success else 1) 