from PIL import Image, ImageDraw, ImageFont
import numpy as np

from network_display.font5x7 import FONT_5x7

def rgb888_to_565(r, g, b):
    """Convert RGB888 to RGB565"""
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

class Framebuffer565:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buf = np.zeros((height, width, 3), dtype=np.uint16)

    def fill(self, color565):
        self.buf[:, :] = color565

    def clear(self, color565):
        self.buf[:, :] = color565

    def draw_pixel(self, x, y, color565):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buf[y, x] = color565

    def draw_line(self, x1, y1, x2, y2, color565):
        dx = abs(x2 - x1)
        dy = -abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx + dy

        while True:
            self.draw_pixel(x1, y1, color565)

            if x1 == x2 and y1 == y2:
                break

            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x1 += sx
            if e2 <= dx:
                err += dx
                y1 += sy

    def draw_text(self, x, y, text, color565):
        px = x
        py = y

        for ch in text:
            if ch == '\n':
                py += 8
                px = x
                continue

            glyph = FONT_5x7.get(ord(ch))
            if glyph is None:
                px += 6
                continue

            # Draw 5x7 glyph
            for row in range(7):
                line = glyph[row]
                for col in range(5):
                    if (line >> (4 - col)) & 1:
                        self.draw_pixel(px + col, py + row, color565)

            px += 6  # spacing


    def draw_rect(self, x, y, w, h, color565):
        self.buf[y:y+h, x:x+w, :] = color565

    def to_rgb888_surface(self):
        """
        Convert internal RGB565 buffer to a 24-bit RGB888 numpy array
        (needed for Pygame testing)
        """
        # arr = self.buf

        # r = (arr >> 11) & 0x1F
        # g = (arr >> 5)  & 0x3F
        # b = arr & 0x1F

        # r = (r << 3).astype(np.uint8)
        # g = (g << 2).astype(np.uint8)
        # b = (b << 3).astype(np.uint8)

        # rgb = np.dstack((r, g, b))
        # return rgb
        # return self.buf.astype(np.uint8)
        return np.transpose(self.buf.astype(np.uint8), (1, 0, 2))

    def get_buffer(self) -> np.array:
        return np.transpose((1, 0, 2))

    def to_rgb565(self):
        """
        Convert the framebuffer (height, width, 3) RGB888 -> RGB565
        Returns bytes in big-endian order suitable for RA8875.
        """
        # Extract RGB channels
        r = ((self.buf[:, :, 0] & 0xF8) << 8).astype(np.uint16)  # 5 bits
        g = ((self.buf[:, :, 1] & 0xFC) << 3).astype(np.uint16)  # 6 bits
        b = (self.buf[:, :, 2] >> 3).astype(np.uint16)  # 5 bits

        # Pack into 16-bit values
        rgb565 = (r << 11) | (g << 5) | b

        # Convert to big-endian byte order
        return rgb565.astype(">u2").tobytes()
