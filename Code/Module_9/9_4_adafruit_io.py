# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import network
import requests
from time import sleep
from machine import Pin

# Wi-Fi credentials
ssid = 'REPLACE_WITH_YOUR_SSID'
password = 'REPLACE_WITH_YOUR_PASSWORD'

# Adafruit IO authentication
username = "ADAFRUIT_IO_USERNAME"
aio_key = "ADAFRUIT_IO_API_KEY"
headers = {'X-AIO-Key': aio_key, 'Content-Type': 'application/json'}

# Adafruit IO feed name for controlling the LED
feed_name = 'raspberry-pi-pico'

# Create the Adafruit IO URL
url = f"https://io.adafruit.com/api/v2/{username}/feeds/{feed_name}/data/last"

# Define the onboard LED pin
led_pin = Pin(20, Pin.OUT)

def init_wifi(ssid, password):# Init Wi-Fi Interface
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
        sleep(1)
    # Check if connection is successful
    if wlan.status() != 3:
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True

def get_led_value():
    try:
        # Get the LED value from Adafruit IO
        response = requests.get(url, headers=headers)
        #Print the response code
        print('Response code: ', response.status_code)
        if (response.status_code == 200):        
            # Get response content
            response_json = response.json()
            # Close the request
            response.close()
            # Print the response
            print(response_json)
            # Get the LED value
            led_value = response_json['value']
            # Print and return the LED value
            print(led_value)
            return led_value
        else:
            return None
    except Exception as e:
        # Handle any exceptions during the request
        print('Error during request:', e)

try:
    if init_wifi(ssid, password):
        while True:
            led_state = get_led_value()
            if led_state == 'ON':
                led_pin.value(1)
            elif led_state == 'OFF':
                led_pin.value(0)
            sleep(1)
            
except KeyboardInterrupt:
    led_pin.value(0)
    print('Keyboard Interrupt')