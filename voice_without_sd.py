import socket
import network
import machine
import uos
import ujson

SSID = "Xjuog"
WIFI_PWD = "11111111"

# compoenets
MICROPHONE_PIN = machine.Pin(32, machine.Pin.IN)

MICROPHONE_PIN = machine.Pin(32, machine.Pin.IN)
SD_CS_PIN = machine.Pin(5, machine.Pin.OUT)
SD_MOSI_PIN = machine.Pin(23, machine.Pin.OUT)
SD_MISO_PIN = machine.Pin(19, machine.Pin.IN)
SD_SCK_PIN = machine.Pin(18, machine.Pin.OUT)

RECORDING_FILE = "/recording.wav"
recording_file = None


def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(ssid, password)

        while not wlan.isconnected():
            pass

    print('Wi-Fi connected!')
    print('IP address:', wlan.ifconfig()[0])


connect_to_wifi(SSID, WIFI_PWD)


def startRecording():
    global recording_file
    print("START_RECORDING..!")
    # Open a file for recording
    try:
        recording_file = open(RECORDING_FILE, "wb")
    except Exception as e:
        print("Error opening recording file:", e)
        return recording_file

    # Start recording from the microphone
    try:
        while True:
            # Convert the pin value to bytes
            data = bytes([MICROPHONE_PIN.value()])
            recording_file.write(data)
    except Exception as e:
        print("Error recording:", e)
        return recording_file


def stopRecordingAndUpload():
    global recording_file
    print("STOP_RECORDING..!")
    # Close the recording file
    try:
        recording_file.close()
    except Exception as e:
        print("Error closing recording file:", e)
        return

    # Upload the recorded audio file to the Django API
    try:
        # Code for uploading the file to Django API
        pass
    except Exception as e:
        print("Error uploading file to API:", e)
        return


def handle_request(client_socket):
    global recording_file
    print('Handling request...')
    request = client_socket.recv(1024).decode()
    print("Received request:", request)  # Debugging statement
    if request:
        method, path, protocol = request.split('\r\n')[0].split(' ')
        print('Method:', method)
        print('Path:', path)
        print('Protocol:', protocol)

        if method == 'POST' and path == '/start-recording':
            recording_file = startRecording()
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nRecording started!'
        elif method == 'POST' and path == '/stop-recording-and-upload':
            stopRecordingAndUpload(recording_file)
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nRecording stopped and uploaded!'
        else:
            response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n404 Page Not Found'

        # Send the HTTP response
        client_socket.send(response.encode())

    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 80))  # Bind to port 80
    server_socket.listen(5)

    print('HTTP server listening on port 80...')

    while True:
        client_socket, addr = server_socket.accept()
        print('Connection from:', addr)
        handle_request(client_socket)


start_server()
