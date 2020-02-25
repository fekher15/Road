from machine import UART
import pycom
import time
from network import LoRa
import socket
import ubinascii
import struct
# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
pycom.heartbeat(False) # turn off heartbeat

uart = UART(0, 115200, bits=8, parity=None, stop=1)
#uart.init(baudrate=115200, bits=8, parity=None, stop=1, timeout=2)
uart.readline()
#uart.write("Connected...")
#uart.read(5)

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
#app_eui = ubinascii.unhexlify('70B3D57ED0018CCD')
#app_key = ubinascii.unhexlify('17BBDE805C5CA9548F575BF35D3E19D1')
app_eui = ubinascii.unhexlify('70B3D57ED0029021')
app_key = ubinascii.unhexlify('70B3D54992D41E2B70B3D54992D41E2B')
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

while not lora.has_joined():
    time.sleep(1.5)
    print('Searching for network...')
    pycom.rgbled(0x000000)
    time.sleep(1.5)
    print("Connected to the network.")
    pycom.rgbled(0xff0000)
# Open LoRaWAN socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)
i = 0
while True:
    if  uart.any():
        data = uart.readline()
        s.send(bytes(data))
        s.setblocking(False)
        data = s.recv(512)
        print ('data')
        pycom.rgbled(0x00FF00) # set LED to RED on if data received
        time.sleep(2.5)
    else:
        print('Sending data...')
        s.send(bytes([0x05, 0xaa, 0xff, 0x88, 0x00, 0x23, 0xdd]))
        print('done.')
        pycom.rgbled(0x000000) # set LED to GREEN if data is b'send'
        time.sleep(2.5)
        i = i + 1
