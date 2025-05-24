# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import network
import requests
import time

# Wi-Fi credentials
ssid = 'REPLACE_WITH_YOUR_SSID'
password = 'REPLACE_WITH_YOUR_PASSWORD'

# Your time zone. List of time zones here: https://timeapi.io/api/TimeZone/AvailableTimeZones
timezone = 'Europe/Lisbon'

url = f'https://timeapi.io/api/Time/current/zone?timeZone={timezone}'

# Init Wi-Fi Interface
def init_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Connect to your network
    wlan.connect(ssid, password)
    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        time.sleep(1)
    # Check if connection is successful
    if wlan.status() != 3:
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True

if init_wifi(ssid, password):
    try:
        response = requests.get(url)
        print('Response code:', response.status_code)
        if response.status_code == 200:
            time_json = response.json()
            print('Response:', time_json)
            date_time = f"{time_json['date']} {time_json['time']}"
            print('Date and Time:', date_time)
        else:
            print('Failed to fetch time data')
            
    except Exception as e:
        print('Error occurred:', e)
        time.sleep(2)
else:
    print('Error connecting to Wi-Fi')
