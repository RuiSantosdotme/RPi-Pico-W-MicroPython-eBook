# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin, ADC
from time import sleep

# Define the ADC pin connected to the LDR
ldr_pin = ADC(2)

# Define the minimum and maximum ADC values for your LDR
min_adc_value = 0
max_adc_value = 65535  # 16-bit ADC

while True:
    # Read the analog value from the LDR
    ldr_value = ldr_pin.read_u16()

    # Map the ADC value to a percentage range
    ldr_percentage = int(((ldr_value - min_adc_value) / (max_adc_value - min_adc_value)) * 100)

    # Print the percentage value
    print("LDR Percentage: {}%".format(ldr_percentage))

    # Add a delay
    sleep(0.5)