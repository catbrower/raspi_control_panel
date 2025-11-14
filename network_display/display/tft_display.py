import board, busio
from adafruit_ra8875 import RA8875

from display import Display

class RA8875Display(Display):
    def __init__(self):
        spi = busio.SPI(board.SCK, board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        rst = digitalio.DigitalInOut(board.D6)

        self.lcd = RA8875(spi, cs, rst, width=800, height=480)
        self.lcd.init()
        self.lcd.display_on(True)

    def clear(self, color=(0, 0, 0)):
        self.lcd.fill(color)

    def draw_pixel(self, x, y, color):
        self.lcd.draw_pixel(x, y, color)

    def draw_line(self, x1, y1, x2, y2, color):
        self.lcd.draw_line(x1, y1, x2, y2, color)

    def draw_text(self, x, y, text, color):
        self.lcd.text(x, y, text, color)

    def update(self):
        pass  # hardware draws instantly

    def show(self):
        pass  # not needed on hardware
