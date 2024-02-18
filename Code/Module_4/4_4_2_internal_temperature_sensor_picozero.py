# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from picozero import pico_temp_sensor

# Convert from celsius to fahrenheit
def celsius_to_fahrenheit(temp_celsius): 
    temp_fahrenheit = temp_celsius * (9/5) + 32 
    return temp_fahrenheit

# Reading and printing the internal temperature
temperature_c = pico_temp_sensor.temp
temperature_f = celsius_to_fahrenheit(temperature_c)

print("Internal Temperature:", temperature_c, "°C")
print("Internal Temperature:", temperature_f, "°F")