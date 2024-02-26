# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin, I2C
from time import sleep
import network
from umqtt.simple import MQTTClient
import config
import BME280

# Define LED
led = Pin('LED', Pin.OUT)

# Constants for MQTT Topics
MQTT_TOPIC_TEMPERATURE = 'pico/temperature'
MQTT_TOPIC_PRESSURE = 'pico/pressure'
MQTT_TOPIC_HUMIDITY = 'pico/humidity'
MQTT_TOPIC_LED = 'pico/led'

# MQTT Parameters
MQTT_SERVER = config.mqtt_server
MQTT_PORT = 0
MQTT_USER = config.mqtt_username
MQTT_PASSWORD = config.mqtt_password
MQTT_CLIENT_ID = b"raspberrypi_picow"
MQTT_KEEPALIVE = 7200
MQTT_SSL = True
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=10000)

# Initialize BME280 sensor
bme = BME280.BME280(i2c=i2c, addr=0x76)

def get_sensor_readings():
    temp = bme.temperature[:-1]
    hum = bme.humidity[:-1]
    pres = bme.pressure[:-3]
    return temp, hum, pres

def initialize_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Connect to the network
    wlan.connect(ssid, password)

    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        sleep(1)

    # Check if connection is successful
    if wlan.status() != 3:
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True

def connect_mqtt():
    try:
        client = MQTTClient(client_id=MQTT_CLIENT_ID,
                            server=MQTT_SERVER,
                            port=MQTT_PORT,
                            user=MQTT_USER,
                            password=MQTT_PASSWORD,
                            keepalive=MQTT_KEEPALIVE,
                            ssl=MQTT_SSL,
                            ssl_params=MQTT_SSL_PARAMS)
        client.connect()
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise  # Re-raise the exception to see the full traceback

def publish_mqtt(topic, value):
    client.publish(topic, value)
    print(topic)
    print(value)
    print("Publish Done")

# Subcribe to MQTT topics
def subscribe(client, topic):
    client.subscribe(topic)
    print('Subscribe to topic:', topic)
    
# Callback function that runs when you receive a message on subscribed topic
def my_callback(topic, message):
    # Perform desired actions based on the subscribed topic and response
    print('Received message on topic:', topic)
    print('Response:', message)
    # Check the content of the received message
    if message == b'ON':
        print('Turning LED ON')
        led.value(1)  # Turn LED ON
    elif message == b'OFF':
        print('Turning LED OFF')
        led.value(0)  # Turn LED OFF
    else:
        print('Unknown command')

try:
    if not initialize_wifi(config.wifi_ssid, config.wifi_password):
        print('Error connecting to the network... exiting program')
    else:
        # Connect to MQTT broker, start MQTT client
        client = connect_mqtt()
        # Assign a callback and subscribe to topics
        client.set_callback(my_callback)
        subscribe(client, MQTT_TOPIC_LED)
        while True:
            # Read sensor data
            temperature, humidity, pressure = get_sensor_readings()

            # Publish as MQTT payload
            publish_mqtt(MQTT_TOPIC_TEMPERATURE, str(temperature))
            publish_mqtt(MQTT_TOPIC_PRESSURE, str(pressure))
            publish_mqtt(MQTT_TOPIC_HUMIDITY, str(humidity))
            
            # Check for new MQTT Messages
            client.check_msg()

            # Delay 5 seconds
            sleep(5)

except Exception as e:
    print('Error:', e)
