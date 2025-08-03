import requests
import re
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# URL of the login page
login_url = "https://172.16.16.16:8090/httpclient.html"

print(f"Analyzing login page: {login_url}")

try:
    # Disable SSL verification for self-signed certificates
    response = requests.get(login_url, verify=False, timeout=10)
    
    if response.status_code == 200:
        html = response.text
        
        # Save the HTML content to a file for inspection
        with open("login_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Saved HTML content to login_page.html")
        
        # Look for forms
        forms = re.findall(r'<form[^>]*>([\s\S]*?)</form>', html)
        print(f"\nFound {len(forms)} form(s)")
        
        for i, form in enumerate(forms):
            print(f"\nForm {i+1}:")
            
            # Extract form attributes
            form_tag = re.search(r'<form[^>]*>', html)
            if form_tag:
                print(f"Form tag: {form_tag.group(0)}")
                
                # Extract form action
                action_match = re.search(r'action=["\']([^"\']+)["\']', form_tag.group(0))
                if action_match:
                    print(f"Form action: {action_match.group(1)}")
                    
                # Extract form method
                method_match = re.search(r'method=["\']([^"\']+)["\']', form_tag.group(0))
                if method_match:
                    print(f"Form method: {method_match.group(1)}")
                    
                # Extract form onsubmit
                onsubmit_match = re.search(r'onsubmit=["\']([^"\']+)["\']', form_tag.group(0))
                if onsubmit_match:
                    print(f"Form onsubmit: {onsubmit_match.group(1)}")
            
            # Extract input fields
            inputs = re.findall(r'<input[^>]*>', form)
            print(f"\nFound {len(inputs)} input field(s) in form {i+1}:")
            
            for j, input_field in enumerate(inputs):
                print(f"\nInput {j+1}: {input_field}")
                
                # Extract input type
                type_match = re.search(r'type=["\']([^"\']+)["\']', input_field)
                if type_match:
                    input_type = type_match.group(1)
                    print(f"Type: {input_type}")
                    
                # Extract input id
                id_match = re.search(r'id=["\']([^"\']+)["\']', input_field)
                if id_match:
                    print(f"ID: {id_match.group(1)}")
                    
                # Extract input name
                name_match = re.search(r'name=["\']([^"\']+)["\']', input_field)
                if name_match:
                    print(f"Name: {name_match.group(1)}")
        
        # If no forms found, look for inputs outside forms
        if not forms:
            print("\nNo forms found. Looking for input fields outside forms...")
            inputs = re.findall(r'<input[^>]*>', html)
            print(f"Found {len(inputs)} input field(s):")
            
            for j, input_field in enumerate(inputs):
                print(f"\nInput {j+1}: {input_field}")
                
                # Extract input type
                type_match = re.search(r'type=["\']([^"\']+)["\']', input_field)
                if type_match:
                    input_type = type_match.group(1)
                    print(f"Type: {input_type}")
                    
                # Extract input id
                id_match = re.search(r'id=["\']([^"\']+)["\']', input_field)
                if id_match:
                    print(f"ID: {id_match.group(1)}")
                    
                # Extract input name
                name_match = re.search(r'name=["\']([^"\']+)["\']', input_field)
                if name_match:
                    print(f"Name: {name_match.group(1)}")
        
        # Look for buttons or input submit elements
        buttons = re.findall(r'<(?:button|input\s+type=["\']submit["\'])[^>]*>', html)
        print(f"\nFound {len(buttons)} button(s):")
        
        for i, button in enumerate(buttons):
            print(f"\nButton {i+1}: {button}")
            
            # Extract button id
            id_match = re.search(r'id=["\']([^"\']+)["\']', button)
            if id_match:
                print(f"ID: {id_match.group(1)}")
                
            # Extract button name
            name_match = re.search(r'name=["\']([^"\']+)["\']', button)
            if name_match:
                print(f"Name: {name_match.group(1)}")
                
            # Extract button onclick
            onclick_match = re.search(r'onclick=["\']([^"\']+)["\']', button)
            if onclick_match:
                print(f"Onclick: {onclick_match.group(1)}")
        
        # Look for elements with onclick attributes that might be login buttons
        onclick_elements = re.findall(r'<[^>]*onclick=["\']([^"\']+)["\'][^>]*>', html)
        login_onclick_elements = []
        for onclick in onclick_elements:
            if 'login' in onclick.lower() or 'submit' in onclick.lower() or 'auth' in onclick.lower():
                login_onclick_elements.append(onclick)
        
        print(f"\nFound {len(login_onclick_elements)} element(s) with login-related onclick:")
        for i, onclick in enumerate(login_onclick_elements):
            print(f"Element {i+1} onclick: {onclick}")
        
        # Look for JavaScript functions that might handle login
        js_functions = re.findall(r'function\s+([^\(]+)\s*\([^\)]*\)\s*\{', html)
        login_functions = [f for f in js_functions if 'login' in f.lower() or 'submit' in f.lower() or 'auth' in f.lower()]
        
        print(f"\nFound {len(login_functions)} login-related JavaScript function(s):")
        for i, func in enumerate(login_functions):
            print(f"Function {i+1}: {func}")
            
            # Try to find the function definition
            func_def = re.search(f"function\s+{re.escape(func)}\s*\([^\)]*\)\s*\{{[\s\S]*?\}}", html)
            if func_def:
                print(f"Function definition: {func_def.group(0)[:200]}...")
        
    else:
        print(f"Failed to access the login page. Status code: {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")