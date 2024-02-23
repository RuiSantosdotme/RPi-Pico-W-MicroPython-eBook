# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import network
import time
import requests

# Wi-Fi credentials
ssid = 'REPLACE_WITH_YOUR_SSID'
password = 'REPLACE_WITH_YOUR_PASSWORD'

api_key = 'REPLACE_WITH_YOUR_API_KEY'
city = 'REPLACE_WITH_YOUR_CITY'
country_code ='REPLACE_WITH_YOUR_COUNTRY_CODE'

# Request URL
url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}'

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
        # Make the request
        response = requests.get(url)
        #Print the response code
        print('Response code: ', response.status_code)
        
        # Get response content
        weather = response.json()
        # Close the request
        response.close()
        
        # Print bulk weather data
        print('Weather JSON: ', weather)
        
        # Get specific weather data
        weather_description = weather['weather'][0]['description']
        print('Current weather: ', weather_description)
        
        # Temperature
        temperature_k = weather['main']['temp']  # Returns temperature in Kelvin
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k - 273.15) * 9/5 + 32
        print(f'Temperature in Kelvin: {temperature_k:.2f}')
        print(f'Temperature in Celsius: {temperature_c:.2f}')
        print(f'Temperature in Fahrenheit: {temperature_f:.2f}')              
        
        # Wind
        wind_speed = weather['wind']['speed']
        print('Wind speed in m/s:', wind_speed)

    except Exception as e:
        # Handle any exceptions during the request
        print('Error during request:', e)
