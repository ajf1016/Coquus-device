import network
import urequests
from machine import Pin
import time

# WiFi credentials
WIFI_SSID = "Xjuog"
WIFI_PASSWORD = "11111111"

# HTTP server URL
SERVER_URL = "https://dummy.restapiexample.com/api/v1/employees"


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


# Make HTTP request
def make_http_request():
    try:
        print("Making HTTP request...")
        response = urequests.get(SERVER_URL)
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
        time.sleep(5)  # Wait for 5 seconds before making the next request


if __name__ == "__main__":
    main()
