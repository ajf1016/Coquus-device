import machine
from sdcard import SDCard
from machine import SoftSPI, Pin

# Initialize SPI
spisd = SoftSPI(-1, miso=Pin(13), mosi=Pin(12), sck=Pin(14))
sd = SDCard(spisd, Pin(27))

# Mount SD card
vfs = os.VfsFat(sd)
os.mount(vfs, '/sd')
