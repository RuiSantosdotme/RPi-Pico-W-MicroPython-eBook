# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import network

# Init WiFi interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Scan for WiFi networks
networks = wlan.scan()

# Print Wi-Fi networks
print("Available WiFi Networks:")
for network_info in networks:
    print(network_info)