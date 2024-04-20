import os
from machine import Pin, SoftSPI
from sdcard import SDCard


spisd = SoftSPI(-1, miso=Pin(13), mosi=Pin(12), sck=Pin(14))
sd = SDCard(spisd, Pin(27))


print('Root dir:{}'.format(os.listdir()))
vfs = os.VfsFat(sd)
os.mount(vfs, '/sd')
print('Root dir:{}'.format(os.listdir()))
os.chdir('sd')
print('sd card contains:{}'.format(os.listdir()))
