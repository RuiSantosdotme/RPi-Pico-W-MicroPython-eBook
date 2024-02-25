# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

# Import necessary modules
import network
from config import wifi_ssid, wifi_password
import socket
import time
from machine import Pin, I2C
import BME280

# Constant variable to save the HTML file path
HTML_FILE_PATH = "webpage.html"

# Create an LED object on pin 'LED'
led = Pin('LED', Pin.OUT)

# Initialize LED state
state = 'OFF'

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=10000)
bme = BME280.BME280(i2c=i2c, addr=0x76)

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

if not init_wifi(wifi_ssid, wifi_password):
    print("Exiting program.")
else:
    try:
        # Set up socket and start listening
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen()
        print('Listening on', addr)

        # Main loop to listen for connections
        while True:
            try:
                conn, addr = s.accept()
                print('Got a connection from', addr)
                
                # Receive and parse the request
                request = conn.recv(1024)
                request_str = request.decode('utf-8')
                print('Request content:')

                try:
                    request = request.split()[1]
                    print('Request:', request)
                except IndexError:
                    pass
                
                # Process the request and update variables
                if request == b'/lighton?':
                    print('LED on')
                    led.value(1)
                    state = 'ON'
                elif request == b'/lightoff?':
                    print('LED off')
                    led.value(0)
                    state = 'OFF'
                    print(state)
                # Generate HTML response
                response = webpage(state)  

                # Send the HTTP response and close the connection
                conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                conn.send(response)
                conn.close()

            except OSError as e:
                conn.close()
                print('Connection closed')
                
    except KeyboardInterrupt:
            print('Server stopped by user.')
