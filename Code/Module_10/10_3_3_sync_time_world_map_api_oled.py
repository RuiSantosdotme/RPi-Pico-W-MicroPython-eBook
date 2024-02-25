# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import network
import requests
import time
from machine import RTC, Timer, SoftI2C, Pin
import ssd1306

# Create a clock to keep track of time
rtc = machine.RTC()

# You can choose any other combination of I2C pins
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

# Set up the OLED display parameters
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Wi-Fi credentials
ssid = 'REPLACE_WITH_YOUR_SSID'
password = 'REPLACE_WITH_YOUR_PASSWORD'

# Your time zone. List of time zones here: https://worldtimeapi.org/timezones
timezone = 'Asia/Dubai'

# API endpoint
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

# Make request to get the time
def get_time():
    try:
        print('Requesting time...')
        response = requests.get(url)
        print('Response code:', response.status_code)
        if (response.status_code == 200):
            time_json= response.json()
            date_time = time_json['datetime']
            
            # Split the datetime string into date and time parts using 'T' as the separator
            date_str, time_str = date_time.split('T')
            print('Date:', date_str)
            print('Time:', time_str)

            # Extract year, month, and day from the date part
            year, month, day = map(int, date_str.split('-'))
            
            # Extract hour, minutes, seconds
            current_time = time_str[:8]
            hour, minute, second = map(int, current_time.split(':'))
            
            # Get current day of week
            day_of_week = time_json['day_of_week']
            
            #Get day of the year
            year_day = time_json['day_of_year']
            
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
            formatted_date = '{:02d}-{:02d}-{:04d}'.format(local_time_tuple[2], local_time_tuple[1], local_time_tuple[0])
            formatted_time = '{:02d}:{:02d}:{:02d}'.format(local_time_tuple[3], local_time_tuple[4], local_time_tuple[5])
            formatted_day_week = days_of_week[local_time_tuple[6]]
            
            print(formatted_day_week)
            print(formatted_date)
            print(formatted_time)
            
            # Clear the OLED display
            oled.fill(0)

            # Display the formatted date and time
            oled.text('Date: ' + formatted_day_week, 0, 0)
            oled.text(formatted_date, 0, 16)
            oled.text('Time: ' + formatted_time, 0, 32)
            oled.show()

            time.sleep(1)
            
        except Exception as e:
            print('Error occurred:', e)
            time.sleep(2)
            continue
