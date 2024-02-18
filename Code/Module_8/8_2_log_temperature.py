# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from time import sleep
from machine import Timer
from picozero import pico_temp_sensor

def log_temperature(timer):
    # Read the internal temperature sensor value
    temperature = pico_temp_sensor.temp

    # Format temperature to a string with two decimal points
    temperature_string = "{:.2f} °C\n".format(temperature)

    # Write to the file
    file_path = 'temperature_log.txt'
    try:
        file = open(file_path, 'a')
        file.write(temperature_string)
        print("Temperature logged successfully.")
        file.close()
    except OSError as e:
        print("Error: ", e)

# Log temperature when the program first runs
log_temperature(0)

# Create a timer that calls log_temperature every minute (60,000 milliseconds)
log_timer = Timer(period=60000, mode=Timer.PERIODIC, callback=log_temperature)

# Keep the program running
try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    # Clean up and stop the timer on keyboard interrupt
    log_timer.deinit()
    print("Keyboard Interrupt")