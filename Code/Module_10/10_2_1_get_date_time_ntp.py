# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import network
import ntptime
import time
from machine import Pin, SoftI2C
import ssd1306

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

# Adjust timezone offset
timezone_offset = 2
timezone_offset_s = timezone_offset*3600

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
    # Synchronize the Pico's internal clock with an NTP server
    ntptime.settime()
    while True:
        try:
            
            # Get the current time in seconds
            current_time = time.time()
            print('Epoch Time:', current_time)
            
            # Adjust timezone
            current_time = current_time + timezone_offset_s

            # Convert the time to a tuple representing the date and time
            time_tuple = time.localtime(current_time)
            print('Time tuple:', time_tuple)
            
            # Format the date and time as strings
            formatted_date = '{:02d}-{:02d}-{:04d}'.format(time_tuple[2], time_tuple[1], time_tuple[0])
            formatted_time = '{:02d}:{:02d}:{:02d}'.format(time_tuple[3], time_tuple[4], time_tuple[5])
            formatted_day_week = days_of_week[time_tuple[6]]

            # Print the date and time
            print("Current date and time:")
            print("Year:", time_tuple[0])
            print("Month:", time_tuple[1])
            print("Day:", time_tuple[2])
            print('Day of the week:', time_tuple[7])
            print("Hour:", time_tuple[3])
            print("Minute:", time_tuple[4])
            print("Second:", time_tuple[5])
            print('Day of the Week:', days_of_week[time_tuple[6]])

            # Clear the OLED display
            oled.fill(0)

            # Display the formatted date and time
            oled.text('Date: ' + formatted_day_week, 0, 0)
            oled.text(formatted_date, 0, 16)
            oled.text('Time: ' + formatted_time, 0, 32)
            oled.show()

            # Print the formatted date and time to the shell
            print('Formatted date:', formatted_date)
            print('Formatted time:', formatted_time)
            
            time.sleep(1)
            
        except Exception as e:
            print('Error occurred:', e)
            time.sleep(2)
            continue
