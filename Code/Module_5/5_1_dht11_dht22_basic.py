# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin
from time import sleep
import dht 

# Create a DHT22 sensor object on GPIO Pin 22
sensor = dht.DHT22(Pin(22))
# Alternatively, you can use DHT11 by uncommenting the line below
# sensor = dht.DHT11(Pin(22))

def celsius_to_fahrenheit(temp_celsius): 
    # Convert temperature from Celsius to Fahrenheit
    temp_fahrenheit = temp_celsius * (9/5) + 32 
    return temp_fahrenheit

while True:
    try:
        sleep(2)
        
        # Measure temperature and humidity
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        # Convert temperature to Fahrenheit
        temp_f = celsius_to_fahrenheit(temp)
        
        # Print sensor readings
        print('DHT Readings: ')
        print('Temperature: %3.1f ºC' % temp)
        print('Temperature: %3.1f ºF' % temp_f)
        print('Humidity: %3.1f %%' % hum)
    
    except OSError as e:
        # Handle sensor reading errors
        print('Failed to read sensor.')