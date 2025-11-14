import pygame

from network_display.display import Display

class PygameDisplay(Display):
    def __init__(self, width=800, height=480, scale=1):
        pygame.init()
        self.width = width
        self.height = height
        self.scale = scale

        # Actual window size (scaled so you can view a small TFT big on screen)
        self.window = pygame.display.set_mode((width*scale, height*scale))
        pygame.display.set_caption("RA8875 Emulator")

        # Internal framebuffer (same size as actual TFT)
        self.surface = pygame.Surface((width, height))

        self.font = pygame.font.SysFont("monospace", 16)

    def clear(self, color=(0,0,0)):
        self.surface.fill(color)

    def draw_pixel(self, x, y, color):
        self.surface.set_at((x, y), color)

    def draw_line(self, x1, y1, x2, y2, color):
        pygame.draw.line(self.surface, color, (x1, y1), (x2, y2))

    def draw_text(self, x, y, text, color):
        img = self.font.render(text, True, color)
        self.surface.blit(img, (x, y))

    def update(self, framebuffer):
        # Scale up for viewing, if needed
        # scaled = pygame.transform.scale(
        #     self.surface,
        #     (self.width * self.scale, self.height * self.scale)
        # )
        # self.window.blit(scaled, (0, 0))
        # pygame.display.flip()
        rgb = framebuffer.to_rgb888_surface()

        # Pygame wants (width, height, 3)
        surf = pygame.surfarray.make_surface(rgb)

        self.window.blit(surf, (0, 0))
        pygame.display.flip()

    def quit(self):
        pass

    def draw_frame(self, framebuffer):
        pass