# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import machine, onewire, ds18x20

# Pin configuration for DS18B20 temperature sensor
ds_pin = machine.Pin(22)

# Create DS18X20 object using OneWire protocol with specified pin
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

# Scan for DS18B20 sensors and print their ROM addresses
rom = ds_sensor.scan()
print('Address:', rom)