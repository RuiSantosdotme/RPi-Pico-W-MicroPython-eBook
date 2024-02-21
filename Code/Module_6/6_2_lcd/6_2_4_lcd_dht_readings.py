# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin, SoftI2C
import dht
from pico_i2c_lcd import I2cLcd
from time import sleep

# Create a DHT22 sensor object on GPIO Pin 22
sensor = dht.DHT22(Pin(22))
# Alternatively, you can use DHT11 by uncommenting the line below
# sensor = dht.DHT11(Pin(22))

# Define the LCD I2C address and dimensions
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C and LCD objects
i2c = SoftI2C(sda=Pin(4), scl=Pin(5), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Byte array for thermometer icon
thermometer = bytearray([0x04, 0x0A, 0x0A, 0x0A, 0x0A, 0x1B, 0x1F, 0x0E])
lcd.custom_char (0, thermometer)

# Byte array for umbrella icon
umbrella = bytearray([0x00, 0x04, 0x0E, 0x1F, 0x04, 0x04, 0x014, 0x0C])
lcd.custom_char (1, umbrella)

def celsius_to_fahrenheit(temp_celsius): 
    # Convert temperature from Celsius to Fahrenheit
    temp_fahrenheit = temp_celsius * (9/5) + 32 
    return temp_fahrenheit

# Display initial message
lcd.putstr("DHT Readings")
sleep(5)

try:
    while True:
        lcd.clear()
        # Measure temperature and humidity
        sensor.measure()
        tempC = sensor.temperature()
        hum = sensor.humidity()
        # Convert temperature to Fahrenheit
        #tempF = celsius_to_fahrenheit(tempC)
        
        # Display temperature
        lcd.putchar(chr(0))
        tempC_lcd = "Temp: " + str(tempC) + "C"
        lcd.putstr(tempC_lcd)
        
        # Display humidity
        lcd.move_to(0, 1)
        lcd.putchar(chr(1))
        hum_lcd = "Hum: " + str(hum) + "%"
        lcd.putstr(hum_lcd)
        
        # Display temperature fahrenheit
        #lcd.putchar(chr(0))
        #tempF_lcd = "Temp: " + str(tempF) + "F"
        #lcd.putstr(tempF_lcd)
        
        # Wait 30 seconds before the next iteration
        sleep(30)
    
except KeyboardInterrupt:
    # Turn off the display when the code is interrupted by the user
    print("Keyboard interrupt")
    lcd.backlight_off()
    lcd.display_off()
