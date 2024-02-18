# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

# Import necessary modules
import network
import asyncio
from config import wifi_ssid, wifi_password
import socket
import time
from machine import Pin, I2C
import BME280

# Constant variable to save the HTML file path
HTML_FILE_PATH = "webpage.html"

# Create several LEDs
led_blink = Pin(20, Pin.OUT)
led_control = Pin(19, Pin.OUT)
onboard_led = Pin('LED', Pin.OUT)

# Initialize LED state
state = 'OFF'

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=10000)
bme = BME280.BME280(i2c=i2c)

# Function to read HTML content from the file
def read_html_file():
    with open(HTML_FILE_PATH, "r") as file:
        return file.read()

# Get sensor readings
def get_readings():
    temp = bme.temperature[:-1]
    hum = bme.humidity[:-1]
    pres = bme.pressure[:-3]
    return temp, hum, pres

# HTML template for the webpage
def webpage(state):
    # Get new sensor readings every time you serve the web page
    temperature, humidity, pressure = get_readings()
    html_content = read_html_file()
    html = html_content.format(state=state, temperature=temperature, humidity=humidity, pressure=pressure)
    print(webpage)
    return html

# Init Wi-Fi Interface
def init_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Connect to your network
    wlan.connect(ssid, password)
    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        print(wlan.status())
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        time.sleep(1)
    # Check if connection is successful
    if wlan.status() != 3:
        print('Failed to connect to Wi-Fi')
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True

# Asynchronous functio to handle client's requests
async def handle_client(reader, writer):
    global state
    
    print("Client connected")
    request_line = await reader.readline()
    print('Request:', request_line)
    
    # Skip HTTP request headers
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line, 'utf-8').split()[1]
    print('Request:', request)
    
    # Process the request and update variables
    if request == '/lighton?':
        print('LED on')
        led_control.value(1)
        state = 'ON'
    elif request == '/lightoff?':
        print('LED off')
        led_control.value(0)
        state = 'OFF'
    
    # Generate HTML response
    response = webpage(state)  

    # Send the HTTP response and close the connection
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()
    print('Client Disconnected')
    
async def blink_led():
    while True:
        led_blink.toggle()  # Toggle LED state
        await asyncio.sleep(0.5)  # Blink interval

async def main():    
    if not init_wifi(wifi_ssid, wifi_password):
        print('Exiting program.')
        return
    
    # Start the server and run the event loop
    print('Setting up server')
    server = asyncio.start_server(handle_client, "0.0.0.0", 80)
    asyncio.create_task(server)
    asyncio.create_task(blink_led())
    
    while True:
        print('Loop')
        # Add other tasks that you might need to do in the loop
        await asyncio.sleep(5)
        onboard_led.toggle()
        
# Create an Event Loop
loop = asyncio.get_event_loop()
# Create a task to run the main function
loop.create_task(main())

try:
    # Run the event loop indefinitely
    loop.run_forever()
except Exception as e:
    print('Error occured: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')