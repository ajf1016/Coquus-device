import socket
import network


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


connect_to_wifi('Xjuog', '11111111')


def handle_request(client_socket):
    print('Handling request...')
    request = client_socket.recv(1024).decode()
    if request:
        print('Received request:', request)
        method, path, protocol = request.split('\r\n')[0].split(' ')
        print('Method:', method)
        print('Path:', path)
        print('Protocol:', protocol)

        if method == 'POST' and path == '/start-recording':
            # Start recording logic here
            print('Recording started!')
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nRecording started!'
        else:
            # Handle other types of requests or return a 404 error
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
        print("CLINET SOCKET", server_socket.accept())
        client_socket, addr = server_socket.accept()
        print('Connection from:', addr)
        handle_request(client_socket)


start_server()
