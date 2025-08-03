import requests
import re
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# URL of the login page
login_url = "https://172.16.16.16:8090/httpclient.html"

print(f"Checking for login button on: {login_url}")

try:
    # Disable SSL verification for self-signed certificates
    response = requests.get(login_url, verify=False, timeout=10)
    
    if response.status_code == 200:
        html = response.text
        
        # Look for buttons or input submit elements
        buttons = re.findall(r'<(?:button|input)[^>]*(?:type=["\']submit["\']|type=["\']button["\'])[^>]*>', html)
        
        print("\nPotential login buttons:")
        for button in buttons:
            print(button)
            
            # Extract ID if present
            id_match = re.search(r'id=["\']([^"\']+)["\']', button)
            if id_match:
                print(f"Button ID: {id_match.group(1)}")
            
            # Extract name if present
            name_match = re.search(r'name=["\']([^"\']+)["\']', button)
            if name_match:
                print(f"Button name: {name_match.group(1)}")
            
            # Extract onclick if present
            onclick_match = re.search(r'onclick=["\']([^"\']+)["\']', button)
            if onclick_match:
                print(f"Button onclick: {onclick_match.group(1)}")
                
            print("---")
        
        # If no buttons found, look for JavaScript functions that might handle login
        if not buttons:
            print("\nNo standard submit buttons found. Looking for JavaScript login functions...")
            js_functions = re.findall(r'function\s+([^\(]+)\s*\([^\)]*\)\s*\{', html)
            login_functions = [f for f in js_functions if 'login' in f.lower() or 'submit' in f.lower() or 'auth' in f.lower()]
            
            print("Potential login functions:")
            for func in login_functions:
                print(f"Function: {func}")
            
            # Look for elements with onclick attributes
            onclick_elements = re.findall(r'<[^>]*onclick=["\']([^"\']+)["\'][^>]*>', html)
            print("\nElements with onclick attributes:")
            for i, onclick in enumerate(onclick_elements):
                if 'login' in onclick.lower() or 'submit' in onclick.lower() or 'auth' in onclick.lower():
                    print(f"Element {i+1} onclick: {onclick}")
            
    else:
        print(f"Failed to access the login page. Status code: {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")