import os
import sys
running_on_pi = True

import pygame

if running_on_pi:
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()

from network_display.display import PygameDisplay, RA8875Display
from network_display.frame_buffer import Framebuffer565

def render(display):
    running = True
    x = 0
    fb = Framebuffer565(800, 480)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            fb.clear((0, 0, 40))
        except Exception as ex:
            print('Error clearing')
            print(ex)
            quit()

        try:
            fb.draw_line(x, 0, x, fb.height, (255,255,0))
        except Exception as ex:
            print('Error line-ing')
            print(ex)
            quit()

        try:
            fb.draw_text(10,10, f"x={x}", (0,255,0))
        except Exception as ex:
            print('Error drawing')
            print(ex)
            quit()

        try:
            display.update(fb)
        except Exception as ex:
            print('Error updating')
            print(ex)

        x = (x + 4) % fb.width

        # display.clear((0, 0, 40))  # dark background

        # # moving line (animation)
        # display.draw_line(x, 0, x, display.height, (255, 255, 0))

        # # Demo text
        # display.draw_text(10, 10, f"x={x}", (0, 255, 0))

        # display.update()

    pygame.quit()


def main():
    print(f'Running on Pi: {running_on_pi}')

    disp = RA8875Display() if running_on_pi else PygameDisplay(800, 480, scale=1)

    try:    
        render(disp)
    except Exception as ex:
        print(ex)
        pygame.quit()
        disp.quit()

if __name__ == '__main__':
    main()