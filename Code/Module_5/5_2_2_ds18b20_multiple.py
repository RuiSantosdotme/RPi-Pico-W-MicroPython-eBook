# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import machine, onewire, ds18x20, time

# Pin configuration for DS18B20 temperature sensor
ds_pin = machine.Pin(22)

# Create DS18X20 object using OneWire protocol with specified pin
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

def celsius_to_fahrenheit(temp_celsius):
    # Convert temperature from Celsius to Fahrenheit
    temp_fahrenheit = temp_celsius * (9/5) + 32 
    return temp_fahrenheit

# Scan for DS18B20 sensors and print their ROM addresses
roms = ds_sensor.scan()
print('Found DS devices: ', roms)
number_devices = len(roms)
print('Number of found devices: ', number_devices)
print('Adresses: ', roms)

while True:
    # Initiate temperature conversion for all sensors
    ds_sensor.convert_temp()
    time.sleep_ms(750)  # Wait for the conversion to complete (750 ms is recommended)

    for rom in roms:
        print(rom)
        
        # Read temperature in Celsius from the sensor
        temp_c = ds_sensor.read_temp(rom)
        
        # Convert Celsius temperature to Fahrenheit
        temp_f = celsius_to_fahrenheit(temp_c)

        # Print the temperature readings
        print('temperature (ºC):', "{:.2f}".format(temp_c))
        print('temperature (ºF):', "{:.2f}".format(temp_f))
        print()

    time.sleep(5)  # Wait for 5 seconds before taking readings again