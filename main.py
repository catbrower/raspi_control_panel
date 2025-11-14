import asyncio
import board
import busio
from digitalio import DigitalInOut
from adafruit_ra8875 import ra8875
from PIL import Image, ImageDraw

# =====================================================================================
# Display Init
# =====================================================================================
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Your pins
cs_pin = DigitalInOut(board.D9)
rst_pin = DigitalInOut(board.D10)

display: ra8875.RA8875 = ra8875.RA8875(spi, cs_pin, rst_pin)
display.init()

# Set your actual panel resolution
WIDTH = 800
HEIGHT = 480

display.backlight = 255


# =====================================================================================
# Pillow → RAW RGB565 → display.blit_buffer
# =====================================================================================
def draw_pillow_image(img: Image.Image):
    """
    Convert a Pillow RGB image to RGB565 and push to RA8875 using blit_buffer().
    """

    # Ensure Pillow image is RGB & matches the screen resolution
    img = img.resize((WIDTH, HEIGHT)).convert("RGB")

    # Convert to RGB565 (5-6-5 bits)
    buf = bytearray(WIDTH * HEIGHT * 2)  # 2 bytes per pixel

    i = 0
    for r, g, b in img.getdata():
        rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        buf[i] = (rgb565 >> 8) & 0xFF      # High byte
        buf[i+1] = rgb565 & 0xFF          # Low byte
        i += 2

    # Push to screen
    display.set_window(0, 0, WIDTH, HEIGHT)
    display.push_pixels(buf)
    # display.blit_buffer(buf, 0, 0, WIDTH, HEIGHT)


# =====================================================================================
# Async update loop
# =====================================================================================
async def update_loop():
    frame = 0

    while True:
        img = Image.new("RGB", (WIDTH, HEIGHT), (255, 0, 255))
        draw = ImageDraw.Draw(img)

        draw.text((20, 20), f"Frame: {frame}", fill=(255, 255, 0))
        draw.rectangle((100, 100, 300 + (frame % 200), 200), outline=(255, 255, 255))

        draw_pillow_image(img)
        frame += 1

        await asyncio.sleep(0.05)  # about 20 FPS


async def main():
    print("Starting async RA8875 Pillow rendering...")
    await update_loop()


asyncio.run(main())
