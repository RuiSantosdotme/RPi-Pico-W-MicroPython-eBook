# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import time
from machine import Pin, SoftI2C
import ssd1306

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# You can choose any other combination of I2C pins
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

# Set up the OLED display parameters
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c, addr=0x3c)

while True:
    # Get the current epoch time
    current_time = time.time()
    print('Epoch Time:', current_time)

    # Convert the time to a time tuple
    time_tuple = time.localtime(current_time)
    print('Time tuple:', time_tuple)

    # Format the date and time as strings
    formatted_date = '{:02d}-{:02d}-{:04d}'.format(time_tuple[2], time_tuple[1], time_tuple[0])
    formatted_time = '{:02d}:{:02d}:{:02d}'.format(time_tuple[3], time_tuple[4], time_tuple[5])
    formatted_day_week = days_of_week[time_tuple[6]]

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

    # Wait for 1 second
    time.sleep(1)
