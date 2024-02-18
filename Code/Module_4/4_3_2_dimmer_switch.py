# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin, PWM, ADC
from time import sleep

# Set up PWM Pin
led_pwm = PWM(Pin(20))

# Set up potentiometer
pot = ADC(Pin(26))

#Set PWM frequency
frequency = 5000
led_pwm.freq (frequency)

try:
    while True:
        # Read potentiometer value and map it to the PWM range
        pot_value = pot.read_u16()
        
        # Turn off the LED for small values
        if pot_value <= 420:
            led_pwm.duty_u16(0)
        else:            
            # Update LED brightness
            led_pwm.duty_u16(pot_value)

        # Add a small delay to avoid rapid changes
        sleep(0.1)
        
except KeyboardInterrupt:
    print("Keyboard interrupt")
    led_pwm.duty_u16(0)
    print(led_pwm)
    led_pwm.deinit()