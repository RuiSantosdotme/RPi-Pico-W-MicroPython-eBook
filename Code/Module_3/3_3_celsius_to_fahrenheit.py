# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

def celsius_to_fahrenheit(temp_celsius):
    temp_fahrenheit = temp_celsius * (9/5) + 32 
    print(temp_fahrenheit)

sensor_temperature = 25
celsius_to_fahrenheit(sensor_temperature)