# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import network

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

print(sta_if.active())
print(ap_if.active())