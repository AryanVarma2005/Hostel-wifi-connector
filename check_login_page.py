import requests
import re

# URL of the login page
login_url = "https://172.16.16.16:8090/httpclient.html"

print(f"Attempting to access login page: {login_url}")

try:
    # Disable SSL verification for self-signed certificates
    response = requests.get(login_url, verify=False, timeout=10)
    
    if response.status_code == 200:
        print(f"Successfully accessed the login page. Status code: {response.status_code}")
        
        # Look for input fields and forms in the HTML
        html = response.text
        
        # Find all input elements
        input_elements = re.findall(r'<input[^>]*>', html)
        print("\nFound input elements:")
        for i, element in enumerate(input_elements):
            print(f"Element {i+1}: {element}")
        
        # Find form elements
        form_elements = re.findall(r'<form[^>]*>.*?</form>', html, re.DOTALL)
        print("\nFound form elements:")
        for i, form in enumerate(form_elements):
            print(f"Form {i+1}: {form[:200]}..." if len(form) > 200 else f"Form {i+1}: {form}")
        
        # Look for potential username/password field IDs
        username_fields = re.findall(r'<input[^>]*(?:user|name|username|login|account)[^>]*>', html, re.IGNORECASE)
        password_fields = re.findall(r'<input[^>]*(?:pass|password|pwd)[^>]*>', html, re.IGNORECASE)
        submit_buttons = re.findall(r'<(?:button|input)[^>]*(?:submit|login|sign)[^>]*>', html, re.IGNORECASE)
        
        print("\nPotential username fields:")
        for field in username_fields:
            print(field)
        
        print("\nPotential password fields:")
        for field in password_fields:
            print(field)
        
        print("\nPotential submit buttons:")
        for button in submit_buttons:
            print(button)
            
    else:
        print(f"Failed to access the login page. Status code: {response.status_code}")
        
except requests.exceptions.SSLError as e:
    print(f"SSL Error: {e}")
    print("This might be due to a self-signed certificate. Try using a browser to inspect the page.")
    
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}")
    print("Could not connect to the server. Please check if the URL is correct and the server is accessible.")
    
except Exception as e:
    print(f"Error: {e}")