# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from micropython import const
import asyncio
import aioble
import bluetooth
import struct
from picozero import pico_temp_sensor

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID('3ac77742-6924-4289-925a-6ad86dfeb618')
# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = bluetooth.UUID('52fcd45e-c477-47d3-9dcf-cc9813795b42')
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

# Register GATT server.
temp_service = aioble.Service(_ENV_SENSE_UUID)
temp_characteristic = aioble.Characteristic(
    temp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True
)
aioble.register_services(temp_service)

# Get temperature and update characteristic
async def write_characteristic_task():
    while True:
        led_state = 'True'
        temp_characteristic.write(led_state, send_update=True)
        print(led_state)
        await asyncio.sleep_ms(1000)

# Serially wait for connections. Don't advertise while a central is connected.
async def peripheral_task():
    while True:
        print("Start advertising")
        try:
            async with await aioble.advertise(
                _ADV_INTERVAL_MS,
                name="RPi-Pico",
                services=[_ENV_SENSE_UUID],
            ) as connection:
                print("Connection from", connection.device)
                await connection.disconnected()
        except asyncio.CancelledError:
            # Catch the CancelledError
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in peripheral_task:", e)
        finally:
            # Ensure the loop continues to the next iteration
            await asyncio.sleep_ms(100)

# Run both tasks.
async def main():
    t1 = asyncio.create_task(write_characteristic_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)

asyncio.run(main())