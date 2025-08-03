import configparser
import os
import getpass
import sys

def update_credentials():
    config_file = 'config.ini'
    
    # Check if config file exists
    if not os.path.exists(config_file):
        print(f"Error: Config file {config_file} not found")
        return False
    
    # Load existing config
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # Get current values
    current_username = config.get('WiFiLogin', 'username')
    current_password = config.get('WiFiLogin', 'password')
    
    # Display current values
    print("=== Update WiFi Login Credentials ===")
    print(f"Current login URL: {config.get('WiFiLogin', 'login_url')}")
    print(f"Current username: {current_username}")
    if current_password == 'your_password':
        print("Current password: [not set]")
    else:
        print("Current password: [hidden]")
    
    print("\nEnter new credentials (leave blank to keep current value)")
    
    # Get new username
    new_username = input("Username: ").strip()
    if not new_username:
        new_username = current_username
    
    # Get new password
    new_password = getpass.getpass("Password: ").strip()
    if not new_password:
        new_password = current_password
    
    # Update config
    config.set('WiFiLogin', 'username', new_username)
    config.set('WiFiLogin', 'password', new_password)
    
    # Save config
    try:
        with open(config_file, 'w') as f:
            config.write(f)
        print("\nCredentials updated successfully!")
        return True
    except Exception as e:
        print(f"\nError saving config: {e}")
        return False

if __name__ == "__main__":
    success = update_credentials()
    
    if success:
        print("\nYou can now run start_wifi_login.bat to start the auto-login process.")
    
    # Keep console open if run directly
    if len(sys.argv) <= 1:
        input("\nPress Enter to exit...")