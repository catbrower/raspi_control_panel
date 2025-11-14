import time

import board
import busio
from busio import SPI
import digitalio

from adafruit_ra8875 import ra8875
from adafruit_ra8875.ra8875 import color565, RA8875

BLACK = color565(0, 0, 0)
RED = color565(255, 0, 0)
BLUE = color565(0, 255, 0)
GREEN = color565(0, 0, 255)
YELLOW = color565(255, 255, 0)
CYAN = color565(0, 255, 255)
MAGENTA = color565(255, 0, 255)
WHITE = color565(255, 255, 255)

# Configuration for CS and RST pins:
cs_pin = digitalio.DigitalInOut(board.D13)
rst_pin = digitalio.DigitalInOut(board.D5)
int_pin = digitalio.DigitalInOut(board.D6)

# Config for display baudrate (default max is 6mhz):
BAUDRATE = 6000000

# Setup SPI bus using hardware SPI:
spi: SPI = SPI(clock = board.SCK, MOSI = board.MOSI, MISO = board.MISO)

# Create and setup the RA8875 display:
display: RA8875 = RA8875(spi, cs = cs_pin, rst = rst_pin, baudrate = BAUDRATE, width = 800, height = 480)
display.init()

display.push_pixels()

time.sleep(1)
display.sleep(True)