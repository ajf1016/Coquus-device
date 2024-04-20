import machine
import time

# Define the GPIO pin connected to the LED
LED_PIN = 2  # You can change this to any GPIO pin you prefer

# Initialize the LED pin as an output
led = machine.Pin(LED_PIN, machine.Pin.OUT)

# Function to toggle the LED


def toggle_led():
    led.value(not led.value())


# Main loop to blink the LED
while True:
    toggle_led()  # Toggle the LED state
    time.sleep(0.5)  # Wait for 0.5 seconds
