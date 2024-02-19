# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)

while True:
    led.value(not led.value())
    sleep(0.5)
