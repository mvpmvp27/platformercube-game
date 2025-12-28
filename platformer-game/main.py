"""
Курсовая работа по дисциплине "Технологии программирования"
Тема: "Игра-платформер 'Кубик-прыгун'"
Студент: Солодков Никита Денисович
Группа: 2121
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

# Импорт классов из папки game_functions
from game_functions.player import Player
from game_functions.platform import Platform
from game_functions.game import Game

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