# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import network
import requests
import time

# Wi-Fi credentials
ssid = 'REPLACE_WITH_YOUR_SSID'
password = 'REPLACE_WITH_YOUR_PASSWORD'

# Your timezone. List of timezones here: https://worldtimeapi.org/timezones
timezone = 'Europe/Lisbon'

url = f'http://worldtimeapi.org/api/timezone/{timezone}'

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
    while True:
        try:
            response = requests.get(url)
            print('Response code:', response.status_code)
            if (response.status_code == 200):
                time_json= response.json()
                print('Response:', time_json)
                date_time = time_json['datetime']
                print('Date and Time:', date_time)
            
        except Exception as e:
            print('Error occurred:', e)
            time.sleep(2)
            continue
