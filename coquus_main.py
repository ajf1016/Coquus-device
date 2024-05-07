import urequests
import network
import socket
from machine import Pin, SoftSPI, SoftI2C
from sdcard import SDCard
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import time
from time import sleep
import os
import json

# WiFi credentials
WIFI_SSID = "Xjuog"
WIFI_PASSWORD = "11111111"

# i2c LCD CONFIGS
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

# File path
RECORD_TIME = 10
# RECORD_TIME = 20
# RECORD_TIME = 30
FILE_PATH = "/sd/audio01.wav"

spisd = SoftSPI(-1, miso=Pin(19), mosi=Pin(23), sck=Pin(18))
sd = SDCard(spisd, Pin(5))

print('Root dir before mounting: {}'.format(os.listdir()))
vfs = os.VfsFat(sd)


def handleLCD(text, t):
    lcd.clear()
    lcd.putstr(text)
    sleep(t)


handleLCD("Audio to text converter", 2)

lcd.clear()
lcd.putstr("Mounting SD Card..")
sleep(3)

try:
    os.mount(vfs, '/sd')
    lcd.clear()
    lcd.putstr("Mounting Done..")
    sleep(1)
except OSError as e:
    lcd.clear()
    lcd.putstr("Mounting FAILED..")
    sleep(1)
    print("Error mounting SD card:", e)

print('Root dir after mounting: {}'.format(os.listdir('/sd')))
os.chdir('/sd')
print('SD card contains: {}'.format(os.listdir()))

# Connect to WiFi


def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        lcd.clear()
        lcd.putstr("Connecting to WiFi...")
        sleep(2)
        print("Connecting to WiFi...")
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print("WiFi connected:", sta_if.ifconfig())
    lcd.clear()
    lcd.putstr("WIFI CONNECTED")
    sleep(1)

# Read audio file from SD card


def read_audio_file():
    try:
        with open(FILE_PATH, "rb") as file:
            audio_data = file.read()
        return audio_data
    except Exception as e:
        print("Error reading audio file:", e)
        return None


def startRecording(record_time):
    handleLCD("Recording started..", 1)
    for i in range(1, RECORD_TIME + 1):
        progress = i * 10
        handleLCD(f"{progress}%", 1)
        # sleep(1)
    handleLCD("Recording completed", 1)


def uploadAudio():
    handleLCD("Uploading", 3)


def deviceConnect():
    handleLCD("SERVER PORT 80  CONNECTED", 1)

# Handle request function


def handle_request(client_socket):
    print('Handling request...')
    request = client_socket.recv(1024).decode()
    if request:
        method, path, protocol = request.split('\r\n')[0].split(' ')
        print('Method:', method)
        print('Path:', path)
        print('Protocol:', protocol)

        if method == 'POST' and path == '/connect':
            deviceConnect()
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nAccess-Control-Allow-Origin: *\r\n\r\nDevice Connected'
        elif method == 'POST' and path == '/start-recording':
            startRecording(RECORD_TIME)
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nAccess-Control-Allow-Origin: *\r\n\r\nRecording started'
        elif method == 'POST' and path == '/upload':
            uploadAudio()
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nAccess-Control-Allow-Origin: *\r\n\r\nRecording started'
        elif method == 'POST' and path == '/stop-recording-and-upload':
            audio_data = read_audio_file()
            if audio_data:
                client_socket.send(audio_data)
                response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nAccess-Control-Allow-Origin: *\r\n\r\nRecording stopped and uploaded'
            else:
                response = 'HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\nAccess-Control-Allow-Origin: *\r\n\r\nError reading audio file'
        else:
            response_from_client = path[1:].replace(
                '%20', ' ') if path.startswith('/') else path.replace('%20', ' ')
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nAccess-Control-Allow-Origin: *\r\n\r\n' + response_from_client

            handleLCD("Note: "+response_from_client, 2)

        # Send the HTTP response
        client_socket.send(response.encode())

    client_socket.close()

# Main function


def main():
    # Connect to WiFi
    connect_to_wifi()

    # Set up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(5)
    print('Server started...')
    lcd.clear()
    lcd.putstr("SERVER STARTED..LISTENING PORT80")
    sleep(2)

    while True:
        client_socket, addr = server_socket.accept()
        handle_request(client_socket)


if __name__ == "__main__":
    main()
