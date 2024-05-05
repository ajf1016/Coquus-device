import network
import urequests
from machine import Pin, SoftSPI
from sdcard import SDCard
import time
import os
import json

# WiFi credentials
WIFI_SSID = "Xjuog"
WIFI_PASSWORD = "11111111"

# HTTP server URL
SERVER_URL = "http://192.168.246.192:8000/api/v1/notes/upload-audio/"

# File path
FILE_PATH = "/sd/02.mp3"

spisd = SoftSPI(-1, miso=Pin(19), mosi=Pin(23), sck=Pin(18))
sd = SDCard(spisd, Pin(5))

print('Root dir before mounting: {}'.format(os.listdir()))
vfs = os.VfsFat(sd)

try:
    os.mount(vfs, '/sd')
except OSError as e:
    print("Error mounting SD card:", e)

print('Root dir after mounting: {}'.format(os.listdir('/sd')))
os.chdir('/sd')
print('SD card contains: {}'.format(os.listdir()))

# Connect to WiFi


def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to WiFi...")
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print("WiFi connected:", sta_if.ifconfig())

# Make HTTP request with file upload


def make_http_request():
    try:
        print("Making HTTP request...")
        with open(FILE_PATH, "rb") as file:
            # Skip reading the entire file into memory, read and send in chunks
            while True:
                chunk = file.read(1024)  # Read 1KB chunk of the file
                if not chunk:
                    break
                # Send the chunk
                response = urequests.post(SERVER_URL, data=chunk, headers={
                                          'Content-Type': 'application/octet-stream'})
                print("HTTP status code:", response.status_code)
                print("Response text:", response.text)
                response.close()
    except Exception as e:
        print("Error making HTTP request:", e)


# Main function
def main():
    connect_to_wifi()
    while True:
        make_http_request()
        time.sleep(10)  # Wait for 5 seconds before making the next request


if __name__ == "__main__":
    main()
