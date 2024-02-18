# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import network
import time
import requests

# Wi-Fi credentials
ssid = 'REPLACE_WITH_YOUR_SSID'
password = 'REPLACE_WITH_YOUR_PASSWORD'

# Request URL
url = 'http://worldtimeapi.org/api/ip'

def init_wifi(ssid, password):
    # Init Wi-Fi Interface
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

def get_time():
    try:
        # Make the request
        response = requests.get(url)
        
        # Print the response code
        print('Response code: ', response.status_code)
        
        # Get response content
        data = response.content
        
        # Get the response as a JSON object
        data_json = response.json()
        print(type(data_json))
        
        # Close the request
        response.close()
        
        # Print the JSON response
        print('JSON Data: ', data_json)
        
        # Extract time information from the response
        current_time = data_json['utc_datetime']
        print('Current UTC time:', current_time)
        week_number = data_json['week_number']
        print('Week number:', week_number)

    except Exception as e:
        # Handle any exceptions during the request
        print('Error during request:', e)

# Continuously display time every second
if init_wifi(ssid, password):
    while True:
        get_time()
        time.sleep(1)