# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

# Import necessary modules
import network
from config import wifi_ssid, wifi_password
import socket
from time import sleep
from machine import Pin, I2C
import BME280

# Create an LED object on pin 'LED'
led = Pin('LED', Pin.OUT)

# Initialize LED state
state = 'OFF'

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=10000)
bme = BME280.BME280(i2c=i2c)

# Get sensor readings
def get_readings():
    temp = bme.temperature[:-1]
    hum = bme.humidity[:-1]
    pres = bme.pressure[:-3]
    return temp, hum, pres

# HTML template for the webpage
def webpage(state):
    #Get new sensor readings every time you serve the web page
    temperature, humidity, pressure = get_readings()
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Raspberry Pi Pico Web Server</h1>
            <h2>Led Control</h2>
            <form action="./lighton">
                <input type="submit" value="Light on" />
            </form>
            <br>
            <form action="./lightoff">
                <input type="submit" value="Light off" />
            </form>
            <p>LED state: {state}</p>
            <h2>BME280 Sensor Readings</h1>
            <p>Temperature: {temperature} &#176C</p>
            <p>Humidity: {humidity} %</p>
            <p>Pressure: {pressure} hPa</p>
            <form action="./">
                <input type="submit" value="Refresh" />
            </form>
        </body>
        </html>
        """
    return str(html)

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
        sleep(1)
    # Check if connection is successful
    if wlan.status() != 3:
        print('her')
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
