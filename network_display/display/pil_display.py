from PIL import Image, ImageDraw, ImageFont

from network_display.display import Display
from network_display.frame_buffer import Framebuffer565

class PILDisplay(Display):
    def __init__(self, width = 800, height = 480):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()

    def clear(self, color=(0, 0, 0)):
        self.draw.rectangle([0, 0, self.width, self.height], fill=color)

    def draw_pixel(self, x, y, color):
        self.draw.point((x, y), fill=color)

    def draw_line(self, x1, y1, x2, y2, color):
        self.draw.line((x1, y1, x2, y2), fill=color)

    def draw_text(self, x, y, text, color):
        self.draw.text((x, y), text, font=self.font, fill=color)

    def update(self, framebuffer:  Framebuffer565) -> None:
        pass

    def show(self):
        self.image.show()  # opens the image in your default viewer

    def quit(self):
        pass
