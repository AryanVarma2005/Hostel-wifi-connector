import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# URL of the login page
login_url = "https://172.16.16.16:8090/httpclient.html"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

print("Opening browser to inspect login page elements...")
print(f"Login URL: {login_url}")

try:
    # Initialize the Chrome driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # Navigate to the login page
    driver.get(login_url)
    
    # Wait for the page to load
    time.sleep(5)
    
    # Get the page source
    page_source = driver.page_source
    
    # Print instructions for the user
    print("\nInspecting login page. Please follow these steps:")
    print("1. Look at the browser window that opened")
    print("2. Right-click on the username field and select 'Inspect' or 'Inspect Element'")
    print("3. Note the 'id' attribute of the input field")
    print("4. Do the same for the password field and login button")
    print("5. Update these values in the config.ini file")
    print("\nThe browser will close automatically after 60 seconds.")
    
    # Keep the browser open for 60 seconds to allow inspection
    time.sleep(60)
    
    # Close the browser
    driver.quit()
    print("Browser closed.")
    
except Exception as e:
    print(f"Error: {e}")
    try:
        driver.quit()
    except:
        pass