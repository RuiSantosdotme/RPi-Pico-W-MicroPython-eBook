# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin, SoftI2C
import ssd1306
import BME280
from time import sleep

# Initialize the I2C connections for OLED and BME280
i2c_oled = SoftI2C(scl=Pin(5), sda=Pin(4))
i2c_bme280 = SoftI2C(scl=Pin(9), sda=Pin(8))

# Set up OLED display parameters
oled_width = 128
oled_height = 64

# Initialize the OLED display
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_oled, addr=0x3c)

while True:
    try:
        # Initialize BME280 sensor
        bme = BME280.BME280(i2c=i2c_bme280, addr=0x76)

        # Clear the OLED display
        oled.fill(0)
        oled.show()

        # Read sensor data from BME280
        tempC = bme.temperature
        hum = bme.humidity
        pres = bme.pressure

        # Convert temperature to Fahrenheit
        tempF = (bme.read_temperature() / 100) * (9 / 5) + 32
        tempF = str(round(tempF, 2)) + 'F'

        # Prepare messages to display on OLED
        tempC_oled = "Temp: " + tempC
        tempF_oled = "Temp: " + tempF
        hum_oled = "Hum: " + hum
        pres_oled = "Pres: " + pres

        # Display sensor readings on OLED
        oled.text(tempC_oled, 0, 0)
        oled.text(tempF_oled, 0, 15)
        oled.text(hum_oled, 0, 30)
        oled.text(pres_oled, 0, 45)

        # Update the OLED display to show the messages
        oled.show()

    except Exception as e:
        # Handle any exceptions during sensor reading
        print('An error occurred:', e)

    # Wait 30 seconds before the next iteration
    sleep(30)
