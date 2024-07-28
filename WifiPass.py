import subprocess
import re

def scan_wifi_networks():
    # Run the 'netsh wlan show networks mode=bssid' command to get a list of available WiFi networks
    networks = subprocess.check_output(['netsh', 'wlan', 'show', 'networks', 'mode=bssid']).decode('utf-8').split('\n')

    # Initialize an empty list to store the network information
    wifi_networks = []

    # Loop through the network list and extract the relevant information
    for network in networks:
        if 'SSID' in network and 'BSSID' in network:
            ssid = network.split(':')[1].strip()
            bssid = network.split(':')[2].strip()
            wifi_networks.append({'SSID': ssid, 'BSSID': bssid})

    return wifi_networks

def get_wifi_password():
    # Run the 'netsh wlan show profiles' command to get a list of saved WiFi profiles
    profiles = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')

    # Initialize an empty dictionary to store the WiFi profiles and passwords
    wifi_profiles = {}

    # Loop through the profiles and extract the profile names
    for profile in profiles:
        if 'All User Profile' in profile:
            profile_name = profile.split(':')[1].strip()
            
            # Run the 'netsh wlan show profile name="profile_name" key=clear' command to get the password
            try:
                password = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', 'name='+profile_name, 'key=clear']).decode('utf-8')
                password_line = re.findall(r'Key Content\s+:\s(.*)', password)[0]
                wifi_profiles[profile_name] = password_line
            except subprocess.CalledProcessError:
                wifi_profiles[profile_name] = 'N/A'

    return wifi_profiles

# Call the functions to get the WiFi networks and profiles/passwords
wifi_networks = scan_wifi_networks()
wifi_passwords = get_wifi_password()

# Print the results
print("Available WiFi Networks:")
for network in wifi_networks:
    print(f"SSID: {network['SSID']}, BSSID: {network['BSSID']}")

print("\nSaved WiFi Profiles and Passwords:")
for profile, password in wifi_passwords.items():
    print(f'Profile: {profile}')
    print(f'Password: {password}')