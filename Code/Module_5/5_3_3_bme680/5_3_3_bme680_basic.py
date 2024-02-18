# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin, I2C
from time import sleep
import bme680

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=10000)

while True:
    try:
        # Initialize BME680 sensor
        bme = bme680.BME680_I2C(i2c=i2c)
        
        # Read sensor data
        temp_celsius = bme.temperature
        temp_fahrenheit = temp_celsius * 9/5 + 32 # Convert to fahrenheit
        humidity = bme.humidity
        pressure = bme.pressure
        gas_resistance = bme.gas / 1000  # Convert Ohms to KOhms
        
        # Print sensor readings
        print('Temperature: {:.2f} °C / {:.2f} °F'.format(temp_celsius, temp_fahrenheit))
        print('Humidity: {:.2f} %'.format(humidity))
        print('Pressure: {:.2f} hPa'.format(pressure))
        print('Gas Resistance: {:.2f} KOhms'.format(gas_resistance))
        print('-------')
        
    except OSError as e:
        # Handle any exceptions during sensor reading
        print('An error occurred:', e)

    sleep(5)