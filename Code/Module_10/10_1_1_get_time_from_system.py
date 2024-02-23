# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import time

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

while True:
    # Get the current time in seconds since the epoch
    current_time = time.time()
    print('Epoch Time:', current_time)

    # Convert the time to a tuple representing the date and time
    time_tuple = time.localtime(current_time)
    print('Time tuple:', time_tuple)

    # Print the date and time
    print('Current date and time:')
    print('Year:', time_tuple[0])
    print('Month:', time_tuple[1])
    print('Day:', time_tuple[2])
    print('Hour:', time_tuple[3])
    print('Minute:', time_tuple[4])
    print('Second:', time_tuple[5])
    print('Day of the Week:', days_of_week[time_tuple[6]])
    
    time.sleep(1)
