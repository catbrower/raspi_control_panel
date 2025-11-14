import time
import board, busio, digitalio
import adafruit_ra8875.registers as reg
from adafruit_ra8875.ra8875 import RA8875, color565

from network_display.display import Display
from network_display.frame_buffer import Framebuffer565

BLACK = color565(0, 0, 0)
WHITE = color565(255, 255, 255)

class RA8875Display(Display):
    def __init__(self):
        self.width = 800
        self.height = 480
        self.scale = 1

        cs = digitalio.DigitalInOut(board.D13)
        rst = digitalio.DigitalInOut(board.D5)
        spi = busio.SPI(clock = board.SCK, MOSI = board.MOSI)
        BAUDRATE = 6000000

        self.display = RA8875(spi, cs, rst, baudrate = BAUDRATE, width = 800, height = 480)
        self.display.init()

    def clear(self, color=(0, 0, 0)):
        self.display.fill(color565(color[0], color[1], color[2]))

    def draw_pixel(self, x, y, color):
        self.display.pixel(x, y, color565(color[0], color[1], color[2]))

    def draw_line(self, x1, y1, x2, y2, color):
        self.display.line(x1, y1, x2, y2, color565(color[0], color[1], color[2]))

    def draw_text(self, x, y, text, color):
        self.display.txt_set_cursor(x, y)
        self.display.txt_trans(WHITE)
        self.display.txt_size(2)
        self.display.txt_write(text)

    def update(self, framebuffer:  Framebuffer565) -> None:
        """
        Write the entire framebuffer to RA8875 at once.
        RA8875 expects big-endian 16-bit RGB565.
        """

        # Convert numpy array to big-endian 16-bit
        data = framebuffer.to_rgb565()
        self.display.set_window(0, 0, self.width, self.height)

        # RA8875 block write
        self.display.push_pixels(data)
        time.sleep(0.2)
        # self.display._wait_poll(reg.MRWC, reg.ST)

    def show(self):
        pass  # not needed on hardware

    def quit(self):
        self.display.sleep(True)
