# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

import json

# Create a dictionary with your data
data = {
    'led_state': True,
    'button_counter': 3
}

# Convert dictionary to a JSON string
json_string = json.dumps(data)
print('JSON String:', json_string)

# Convert JSON string back to micropython object
parsed_data = json.loads(json_string)
print('Parsed data: ', parsed_data)
print(type(parsed_data))

led_state = parsed_data['led_state']
print('LED State:', led_state, ', variable type:', type(led_state))

button_counter = parsed_data['button_counter']
print('Button Counter: ', button_counter, ', variable type', type(button_counter))