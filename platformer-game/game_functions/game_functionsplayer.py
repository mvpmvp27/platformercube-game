import pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)

class Player:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.jump_power = -14
        self.gravity = 0.75
        self.on_ground = False
        self.color = BLUE
        self.trail = []
        self.trail_length = 10
        self.move_speed = 5

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

    def update(self, platforms):
        self.vel_y += self.gravity
        self.x += self.vel_x
        self.y += self.vel_y

        self.trail.append((self.x + self.width // 2, self.y + self.height // 2))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

        if self.y > SCREEN_HEIGHT:
            return False

        self.on_ground = False

        for platform in platforms:
            if self.x + self.width > platform.x and self.x < platform.x + platform.width:
                if self.vel_y > 0 and self.y + self.height <= platform.y + 10 and self.y + self.height + self.vel_y >= platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    break

        return True

    def draw(self, screen):
        for i, pos in enumerate(self.trail):
            alpha_factor = i / len(self.trail)
            size = int(15 * alpha_factor)
            pygame.draw.circle(screen, (100, 200, 255), pos, size, 1)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)

        eye_size = 6
        pygame.draw.circle(screen, WHITE, (self.x + 12, self.y + 14), eye_size)
        pygame.draw.circle(screen, WHITE, (self.x + 28, self.y + 14), eye_size)
        pygame.draw.circle(screen, BLACK, (self.x + 12, self.y + 14), eye_size // 2)
        pygame.draw.circle(screen, BLACK, (self.x + 28, self.y + 14), eye_size // 2)