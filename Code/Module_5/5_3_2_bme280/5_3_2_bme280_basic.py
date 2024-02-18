# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin, I2C
from time import sleep
import BME280

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=10000)

while True:
    try:
        # Initialize BME280 sensor
        bme = BME280.BME280(i2c=i2c)
        
        # Read sensor data
        temp_c = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
        
        # Convert temperature to fahrenheit
        temp_f = (bme.read_temperature()/100) * (9/5) + 32
        temp_f = str(round(temp_f, 2)) + 'F'
        
        # Print sensor readings
        print('Temperature: ', temp_c)
        print('Temperature: ', temp_f)
        print('Humidity: ', hum)
        print('Pressure: ', pres)
        
    except Exception as e:
        # Handle any exceptions during sensor reading
        print('An error occurred:', e)

    sleep(5)