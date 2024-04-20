import os
from machine import Pin, SoftSPI
from sdcard import SDCard


# Initialize SPI and SD card
spisd = SoftSPI(-1, miso=Pin(13), mosi=Pin(12), sck=Pin(14))
sd = SDCard(spisd, Pin(27))

print('Root dir before mounting: {}'.format(os.listdir()))
vfs = os.VfsFat(sd)

try:
    os.mount(vfs, '/sd')
except OSError as e:
    print("Error mounting SD card:", e)

print('Root dir after mounting: {}'.format(os.listdir('/sd')))
os.chdir('/sd')
print('SD card contains: {}'.format(os.listdir()))

# Create a sample file
with open('/sd/sample.txt', 'w') as f:
    f.write("This is a sample file.")

# Read the sample file
with open('/sd/sample.txt', 'r') as f:
    content = f.read()
    print("Content of sample.txt:", content)
