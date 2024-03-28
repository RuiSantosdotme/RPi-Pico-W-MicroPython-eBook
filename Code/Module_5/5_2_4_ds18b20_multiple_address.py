# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import machine, onewire, ds18x20, time

# Pin configuration for DS18B20 temperature sensor
ds_pin = machine.Pin(22)

# Create DS18X20 object
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

def celsius_to_fahrenheit(temp_celsius):
    # Convert temperature from Celsius to Fahrenheit
    temp_fahrenheit = temp_celsius * (9/5) + 32 
    return temp_fahrenheit

# Dictionary with sensor names and their ROM addresses
sensor_address = {
    "Sensor1": bytearray(b'(\xff\xa0\x113\x17\x03\x96'),
    "Sensor2": bytearray(b'(\xff\x11(3\x18\x01k'),
    "Sensor3": bytearray(b'(\xff\xb4\x063\x17\x03K'),
    "Sensor4": bytearray(b'(\xff\x1e\x133\x17\x03|'),
    # Add or remove sensors as needed
}

while True:
    # Initiate temperature conversion for all sensors
    ds_sensor.convert_temp()
    time.sleep_ms(750)  # Wait for the conversion to complete
    for sensor_name, address in sensor_address.items():
        # Print the sensor name
        print("Sensor Name:", sensor_name)

        # Read temperature in Celsius from the specified sensor
        temp_c = ds_sensor.read_temp(address)

        # Convert Celsius temperature to Fahrenheit
        temp_f = celsius_to_fahrenheit(temp_c)

        # Print the temperature readings
        print('Temperature (ºC):', "{:.2f}".format(temp_c))
        print('Temperature (ºF):', "{:.2f}".format(temp_f))
        print()

    time.sleep(5)
