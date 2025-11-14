import board, busio, digitalio
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

        self.lcd = RA8875(spi, cs, rst, baudrate = BAUDRATE, width = 800, height = 480)
        self.lcd.init()

    def clear(self, color=(0, 0, 0)):
        self.lcd.fill(color565(color[0], color[1], color[2]))

    def draw_pixel(self, x, y, color):
        self.lcd.pixel(x, y, color565(color[0], color[1], color[2]))

    def draw_line(self, x1, y1, x2, y2, color):
        self.lcd.line(x1, y1, x2, y2, color565(color[0], color[1], color[2]))

    def draw_text(self, x, y, text, color):
        self.lcd.txt_set_cursor(x, y)
        self.lcd.txt_trans(WHITE)
        self.lcd.txt_size(2)
        self.lcd.txt_write(text)

    def update(self, framebuffer:  Framebuffer565) -> None:
        """
        Write the entire framebuffer to RA8875 at once.
        RA8875 expects big-endian 16-bit RGB565.
        """

        # Convert numpy array to big-endian 16-bit
        data = framebuffer.to_rgb565()
        self.lcd.set_window(0, 0, self.width, self.height)

        # RA8875 block write
        self.lcd.push_pixels(data)

    def show(self):
        pass  # not needed on hardware

    def quit(self):
        self.lcd.sleep(True)
