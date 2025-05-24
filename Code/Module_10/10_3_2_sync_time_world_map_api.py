# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import network
import requests
import time
from machine import RTC, Timer

# Create a clock to keep track of time
rtc = machine.RTC()

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                'Friday', 'Saturday', 'Sunday']

# Wi-Fi credentials
ssid = 'REPLACE_WITH_YOUR_SSID'
password = 'REPLACE_WITH_YOUR_PASSWORD'

# Your time zone. List of time zones here: https://timeapi.io/api/TimeZone/AvailableTimeZones
timezone = 'Europe/Lisbon'

# API endpoint
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
    
# Make request to get the time
def get_time():
    try:
        print('Requesting time...')
        response = requests.get(url)
        print('Response code:', response.status_code)
        if (response.status_code == 200):
            time_json= response.json()
            
            year = time_json['year']
            month = time_json['month']
            day = time_json['day']
            day_of_week = time_json['dayOfWeek']
            hour = time_json['hour']
            minute = time_json['minute']
            second = time_json['seconds']
            
            # Put together the time tuple
            time_tuple =(year, month, day, day_of_week, hour, minute, second, 0)
            
            return time_tuple
        
    except Exception as e:
        print('An error occurred', e)
    finally:
        response.close()
        
# Synchronize the time
def set_time(timer):
    time_tuple = get_time()
    rtc.datetime(time_tuple)
    print('Sync time')

# Periodically call set_time to synchronize the time
sync_time_timer = Timer()
sync_time_timer.init(mode=Timer.PERIODIC, period=100000, callback=set_time)

# Get Current Date and Time    
if init_wifi(ssid, password):
    # Synchronize the clock
    set_time(0)
    while True:
        try:
            # Get current time
            current_time = time.time()
            # Convert the time to a time tuple
            local_time_tuple = time.localtime(current_time)
            print(local_time_tuple)
            # Format the date and time as strings
            formatted_date = '{:02d}-{:02d}-{:04d}'.format(local_time_tuple[2],
                             local_time_tuple[1], local_time_tuple[0])
            formatted_time = '{:02d}:{:02d}:{:02d}'.format(local_time_tuple[3],
                             local_time_tuple[4], local_time_tuple[5])
            formatted_day_week = days_of_week[local_time_tuple[6]]
            
            print(formatted_day_week)
            print(formatted_date)
            print(formatted_time)
            
            time.sleep(1)
            
        except Exception as e:
            print('Error occurred:', e)
            time.sleep(2)
            continue
