import pygame

PLATFORM_COLOR = (100, 180, 100)

class Platform:
    def __init__(self, x, y, width, color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20
        self.color = color if color else PLATFORM_COLOR

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen,
                         tuple(min(c + 40, 255) for c in self.color),
                         (self.x, self.y, self.width, 5))
        pygame.draw.rect(screen,
                         tuple(max(c - 50, 0) for c in self.color),
                         (self.x, self.y + self.height - 3, self.width, 3))
