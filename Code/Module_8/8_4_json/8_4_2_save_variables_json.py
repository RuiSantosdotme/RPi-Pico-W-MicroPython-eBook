# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin
import os
import json

# File path where we want to save the variables
FILE_PATH = 'data.json'

# Intialize the LED and the button
led = Pin(20, Pin.OUT)
button = Pin(21, Pin.IN, Pin.PULL_DOWN)
counter = 0  # Initialize the button press count

# Function to save data to a JSON file
def save_data(led_value, button_counter):
    state = {
        'led_value': led_value,
        'button_counter': button_counter
    }
    try:
        with open(FILE_PATH, 'w') as file:
            json.dump(state, file)
            print('State saved successfully.')
    except Exception as e:
        print('Error saving state: ', e)

# Function to load data from a JSON file
def load_data():
    try:
        # Check if the file exists before attempting to open
        if FILE_PATH in os.listdir():
            with open(FILE_PATH, 'r') as file:
                state = json.load(file)
                print('State loaded successfully.')
                return state
        else:
            print('State file not found. Returning default values.')
            return {'led_value': False, 'button_counter': 0}
            
    except Exception as e:
        print('Error loading state: ', e)
        return None

# Toggle LED and save state on each button press
def button_pressed(pin):
    global counter  # Declare variable as global
    counter += 1
    print('Button Pressed! Count:', counter)

    # Toggle the LED on each button press
    led.value(not led.value())

    # Save the current led state and counter value to a file
    save_data(led.value(), counter)

# Attach the interrupt to the button's rising edge
button.irq(trigger=Pin.IRQ_RISING, handler=button_pressed)

# Load the initial data when the script starts
data = load_data()
if data is not None:
    led_value = data['led_value']
    led.value(led_value)
    counter = data['button_counter']
    print('LED VALUE: ', led_value, 'COUNTER VALUE: ', counter)

# Keep the program running
try:
    while True:
        pass
except KeyboardInterrupt:
    print('Keyboard Interrupt')
