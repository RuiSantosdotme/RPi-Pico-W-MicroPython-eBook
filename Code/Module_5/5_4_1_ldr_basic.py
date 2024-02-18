# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin, ADC
from time import sleep

# Define the ADC pin connected to the LDR
ldr_pin = ADC(2)

while True:
    # Read the analog value from the LDR
    ldr_value = ldr_pin.read_u16()

    # Print the analog value
    print("LDR Value:", ldr_value)

    # Add a delay
    sleep(0.5)