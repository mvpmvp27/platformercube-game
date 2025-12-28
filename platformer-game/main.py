"""
Курсовая работа по дисциплине "Технологии программирования"
Тема: "Игра-платформер 'Кубик-прыгун'"
Студент: Солодков Никита Денисович
Группа: 2122
Преподаватель: Елсакова А. В.
"""
import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
BLUE = (50, 150, 255)
ORANGE = (255, 150, 50)
PURPLE = (180, 70, 220)
BACKGROUND_COLOR = (30, 30, 40)
PLATFORM_COLOR = (100, 180, 100)

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

        # След
        self.trail.append((self.x + self.width // 2, self.y + self.height // 2))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

        # Ограничение по краям
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

        # Падение за экран
        if self.y > SCREEN_HEIGHT:
            return False

        # СБРОС состояния ground перед проверкой
        self.on_ground = False

        # Проверяем коллизии ТОЛЬКО сверху вниз
        for platform in platforms:
            # Проверка пересечения по горизонтали
            if self.x + self.width > platform.x and self.x < platform.x + platform.width:
                # Проверка, что игрок падает и его нижняя грань ниже верха платформы
                if self.vel_y > 0 and self.y + self.height <= platform.y + 10 and self.y + self.height + self.vel_y >= platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    break  # достаточно одной платформы

        return True

    def draw(self, screen):
        # След
        for i, pos in enumerate(self.trail):
            alpha_factor = i / len(self.trail)
            size = int(15 * alpha_factor)
            pygame.draw.circle(screen, (100, 200, 255), pos, size, 1)

        # Кубик
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)

        # Глаза
        eye_size = 6
        pygame.draw.circle(screen, WHITE, (self.x + 12, self.y + 14), eye_size)
        pygame.draw.circle(screen, WHITE, (self.x + 28, self.y + 14), eye_size)
        pygame.draw.circle(screen, BLACK, (self.x + 12, self.y + 14), eye_size // 2)
        pygame.draw.circle(screen, BLACK, (self.x + 28, self.y + 14), eye_size // 2)


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


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Кубик-прыгун - Курсовая работа")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.keys = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_a: False,
            pygame.K_d: False
        }
        self.reset_game()

    def reset_game(self):
        self.platforms = []
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.platform_speed = 2.0
        self.last_platform_y = SCREEN_HEIGHT - 100
        self.waiting_for_first_jump = True

        # Стартовая платформа
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, (80, 150, 80))
        self.platforms.append(ground)

        # Игрок ТОЧНО на платформе
        self.player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 80)
        self.player.on_ground = True

        # Генерация начальных платформ с уменьшенным шагом
        for _ in range(6):
            x = random.randint(50, SCREEN_WIDTH - 150)
            # ←←← ВАЖНО: уменьшен вертикальный шаг до 80–110 пикселей
            y = self.last_platform_y - random.randint(80, 110)
            w = random.randint(100, 200)
            color = random.choice([GREEN, ORANGE, PURPLE, (120, 210, 180)])
            self.platforms.append(Platform(x, y, w, color))
            self.last_platform_y = y

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as f:
            f.write(str(self.high_score))

    def generate_platform(self):
        if self.last_platform_y > 150:
            x = random.randint(50, SCREEN_WIDTH - 150)
            # ←←← Уменьшён шаг при генерации
            y = self.last_platform_y - random.randint(80, 110)
            w = random.randint(100, 180)
            color = random.choice([GREEN, ORANGE, PURPLE, (140, 220, 160)])
            self.platforms.append(Platform(x, y, w, color))
            self.last_platform_y = y

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.keys[pygame.K_LEFT] = True
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.keys[pygame.K_RIGHT] = True
                elif event.key == pygame.K_UP:
                    if not self.game_over:
                        self.player.jump()
                        if self.waiting_for_first_jump:
                            self.waiting_for_first_jump = False
                elif event.key == pygame.K_r:
                    if self.game_over:
                        self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.keys[pygame.K_LEFT] = False
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.keys[pygame.K_RIGHT] = False

    def update(self):
        if self.game_over:
            return

        # Управление
        self.player.vel_x = 0
        if self.keys[pygame.K_LEFT]:
            self.player.vel_x = -self.player.move_speed
        if self.keys[pygame.K_RIGHT]:
            self.player.vel_x = self.player.move_speed

        # Двигаем платформы ТОЛЬКО после первого прыжка
        if not self.waiting_for_first_jump:
            for p in self.platforms:
                p.y += self.platform_speed

            # Удаляем ушедшие платформы
            self.platforms = [p for p in self.platforms if p.y > -50]

            # Генерируем новые
            if self.platforms and self.platforms[-1].y > 150:
                self.generate_platform()

        # Обновляем игрока
        alive = self.player.update(self.platforms)
        if not alive:
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

        # Счёт и центрирование
        if not self.waiting_for_first_jump and self.player.y < SCREEN_HEIGHT // 2:
            self.score += 1
            self.player.y = SCREEN_HEIGHT // 2

        # Увеличение сложности
        if self.score > 1500 and self.score % 500 == 0:
            self.platform_speed = min(self.platform_speed + 0.1, 3.5)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        # Звёзды
        for i in range(60):
            x = (i * 71) % SCREEN_WIDTH
            y = (i * 53 + pygame.time.get_ticks() // 50) % (SCREEN_HEIGHT + 100) - 50
            size = (i % 3) + 1
            bright = 150 + (i % 105)
            pygame.draw.circle(self.screen, (bright, bright, bright), (x, y), size)

        # Платформы и игрок
        for platform in self.platforms:
            platform.draw(self.screen)
        self.player.draw(self.screen)

        # Интерфейс
        score_text = self.font.render(f"Счёт: {self.score}", True, WHITE)
        high_text = self.font.render(f"Рекорд: {self.high_score}", True, ORANGE)
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(high_text, (20, 50))

        if not self.game_over:
            if self.waiting_for_first_jump:
                hint = self.font.render("Нажмите ↑, чтобы начать!", True, GREEN)
                self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 20))
            else:
                inst = self.font.render("←→ или A/D — движение | ↑ — прыжок", True, GREEN)
                self.screen.blit(inst, (SCREEN_WIDTH - 420, 20))

        # Экран проигрыша
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            self.screen.blit(overlay, (0, 0))

            go = self.big_font.render("ИГРА ОКОНЧЕНА", True, RED)
            sc = self.font.render(f"Ваш счёт: {self.score}", True, WHITE)
            hs = self.font.render(f"Рекорд: {self.high_score}", True, ORANGE)
            rst = self.font.render("R — новая игра", True, GREEN)
            esc = self.font.render("ESC — выход", True, WHITE)

            self.screen.blit(go, (SCREEN_WIDTH // 2 - go.get_width() // 2, 210))
            self.screen.blit(sc, (SCREEN_WIDTH // 2 - sc.get_width() // 2, 290))
            self.screen.blit(hs, (SCREEN_WIDTH // 2 - hs.get_width() // 2, 330))
            self.screen.blit(rst, (SCREEN_WIDTH // 2 - rst.get_width() // 2, 380))
            self.screen.blit(esc, (SCREEN_WIDTH // 2 - esc.get_width() // 2, 420))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    print("=" * 50)
    print("Игра 'Кубик-прыгун'")
    print("Курсовая работа по технологиям программирования")
    print("=" * 50)
    print("Управление:")
    print("  ← → или A/D - движение влево/вправо")
    print("  ↑ (стрелка вверх) - прыжок (нажмите, чтобы начать)")
    print("  R - перезапуск (только после проигрыша)")
    print("  ESC - выход")
    print("=" * 50)
    game = Game()

    game.run()
