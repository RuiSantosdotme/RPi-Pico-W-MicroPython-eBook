# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import os

dir_path = 'my_directory'

# List the files in the directory
files = os.listdir(dir_path)
print("Files in the directory:", files)