import board, busio, digitalio
from adafruit_ra8875.ra8875 import RA8875, color565

from network_display.display import Display

BLACK = color565(0, 0, 0)
WHITE = color565(255, 255, 255)

class RA8875Display(Display):
    def __init__(self):
        cs = digitalio.DigitalInOut(board.D13)
        rst = digitalio.DigitalInOut(board.D5)
        spi = busio.SPI(clock = board.SCK, MOSI = board.MOSI)
        BAUDRATE = 6000000

        self.lcd = RA8875(spi, cs, rst, baudrate = BAUDRATE, width = 800, height = 480)
        self.lcd.init()

    def clear(self, color=(0, 0, 0)):
        self.lcd.fill(color565(**color))

    def draw_pixel(self, x, y, color):
        self.lcd.pixel(x, y, color)

    def draw_line(self, x1, y1, x2, y2, color):
        self.lcd.line(x1, y1, x2, y2, color)

    def draw_text(self, x, y, text, color):
        self.lcd.txt_set_cursor(x, y)
        self.lcd.txt_trans(WHITE)
        self.lcd.txt_size(2)
        self.lcd.txt_write(text)

    def update(self):
        pass  # hardware draws instantly

    def show(self):
        pass  # not needed on hardware
