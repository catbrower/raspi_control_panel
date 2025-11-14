
import pygame

from network_display.display import PygameDisplay, RA8875Display

def render(display):
    running = True
    x = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display.clear((0, 0, 40))  # dark background

        # moving line (animation)
        display.draw_line(x, 0, x, display.height, (255, 255, 0))

        # Demo text
        display.draw_text(10, 10, f"x={x}", (0, 255, 0))

        x = (x + 2) % display.width

        display.update()

    pygame.quit()


def main():
    running_on_pi = True

    if running_on_pi:
        disp = RA8875Display()
    else:
        disp = PygameDisplay(800, 480, scale=1)

        
    render(disp)
    # disp = PILDisplay(800, 480)
    # disp.clear((0, 0, 255))
    # disp.draw_text(50, 50, "Hello RA8875 emulator!", (255, 255, 0))
    # disp.draw_line(0, 0, 799, 479, (255, 0, 0))
    # disp.show()
