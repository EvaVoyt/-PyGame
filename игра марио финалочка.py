import pygame
import sys
from pygame.locals import *
import random
import time

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Клетчатое поле - Собери монетки!")

# Цвета
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Размеры клетки
TILE_SIZE = 50

# Создание игрового поля
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# Загрузка изображений
player_image = pygame.image.load("data/mario.png")   # Изображение игрока
coin_image = pygame.image.load("data/star.png")      # Изображение монетки
wall_image = pygame.image.load("data/box.png")      # Изображение стены
enemy_image = pygame.image.load("data/dragon.png")    # Изображение врага
grass_image = pygame.image.load("data/grass.png")    # Изображение травы
flag_image = pygame.image.load("data/flag.png")    # Изображение травы
fire_image = pygame.image.load("data/fireball.png")  # Изображение огонька


# Масштабирование изображений под размер клетки
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
coin_image = pygame.transform.scale(coin_image, (TILE_SIZE, TILE_SIZE))
wall_image = pygame.transform.scale(wall_image, (TILE_SIZE, TILE_SIZE))
enemy_image = pygame.transform.scale(enemy_image, (TILE_SIZE, TILE_SIZE))
grass_image = pygame.transform.scale(grass_image, (TILE_SIZE, TILE_SIZE))
flag_image = pygame.transform.scale(flag_image, (TILE_SIZE, TILE_SIZE))
fire_image = pygame.transform.scale(fire_image, (TILE_SIZE, TILE_SIZE))
# Определение уровней
levels = [
    [
        'WWWWWWWWWWWWWWWW',
        'W   C     P    W',
        'W              W',
        'W   W     E    W',
        'W   W          W',
        'W   C     W    W',
        'W  E           W',
        'W   W          W',
        'W   C     W    W',
        'W  E           W',
        'W        C    FW',
        'WWWWWWWWWWWWWWWW',
    ],
    [
        'WWWWWWWWWWWWWWWW',
        'W   C      E   W',
        'W       C      W',
        'W   W     C    W',
        'W  E      W    W',
        'W  E C         W',
        'W              W',
        'W   W    C     W',
        'W   C          W',
        'W  E       P   W',
        'W       C     FW',
        'WWWWWWWWWWWWWWWW',
    ],
    [
        'WWWWWWWWWWWWWWWW',
        'W  E       E   W',
        'W       C      W',
        'W   W     C    W',
        'W  E      W    W',
        'W  E C       E W',
        'W P         С  W',
        'W   W    C     W',
        'W   C          W',
        'W   E          W',
        'W P       C   FW',
        'WWWWWWWWWWWWWWWW',
    ]
]
# Функция для отображения окна после уровня
def show_level_result(screen, message, color):
    screen.fill((156, 180, 100))  # Зеленый фон
    font = pygame.font.Font(None, 48)  # Создаем шрифт большего размера
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()  # Обновляем экран
    time.sleep(2)  # Ждем 2 секунды

# Класс игрока
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, walls):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_y < len(walls) and 0 <= new_x < len(walls[0]):
            if not walls[new_y][new_x]:
                self.x = new_x
                self.y = new_y

    def draw(self, surface):
        surface.blit(player_image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

# Класс монетки
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            surface.blit(coin_image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

class Flag:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def draw(self, surface):
        surface.blit(flag_image, (self.x * TILE_SIZE, self.y * TILE_SIZE))


# Класс для огоньков
class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # Направление движения (1 - вправо, -1 - влево)

    def move(self):
        self.x += self.direction  # Двигаемся в указанном направлении

    def draw(self, surface):
        # Отрисовываем изображение огонька вместо красного квадрата
        surface.blit(fire_image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

# Класс врага с возможностью возрождения
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.facing_right = True  # True, если движется вправо
        self.image = enemy_image  # Изначальное изображение

    def move(self, walls):
        new_x = self.x + (1 if self.facing_right else -1)

        # Проверяем, находится ли новая позиция в пределах поля и не является ли она стеной
        if 0 <= new_x < len(walls[0]) and not walls[self.y][new_x]:
            self.x = new_x  # Двигаемся вперед
        else:
            self.facing_right = not self.facing_right  # Меняем направление взгляда
            self.update_image()  # Обновляем изображение

    def update_image(self):
        self.image = pygame.transform.flip(enemy_image, not self.facing_right, False)

    def respawn(self, walls):
        # Находим случайную свободную клетку для возрождения
        while True:
            new_x = random.randint(0, GRID_WIDTH - 1)
            new_y = random.randint(0, GRID_HEIGHT - 1)
            if not walls[new_y][new_x]:
                self.x = new_x
                self.y = new_y
                break

    def draw(self, surface):
        surface.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

# Функция отображения текста
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Функция загрузки уровня
def load_level(level_index):
    level_data = levels[level_index]
    player_x, player_y = 0, 0
    coins = []
    enemies = []
    walls = []
    flag = None  # Переменная для хранения флага
    for row_index, row in enumerate(level_data):
        wall_row = []
        for col_index, cell in enumerate(row):
            if cell == 'P':  # Игрок
                player_x, player_y = col_index, row_index
                wall_row.append(False)
            elif cell == 'C':  # Монетка
                coins.append(Coin(col_index, row_index))
                wall_row.append(False)
            elif cell == 'W':  # Стена
                wall_row.append(True)
            elif cell == 'E':  # Враг
                enemies.append(Enemy(col_index, row_index))
                wall_row.append(False)
            elif cell == 'F':  # Флаг
                flag = Flag(col_index, row_index)  # Создаем объект флага
                wall_row.append(False)
            else:  # Пустое место
                wall_row.append(False)
        walls.append(wall_row)
    player = Player(player_x, player_y)
    return player, coins, enemies, walls, flag  # Возвращаем флаг

# Функция стартового окна
def start_screen():
    while True:
        screen.fill((156, 180, 100))  # Зеленый фон
        draw_text("Чтобы начать игру, нажмите пробел", font, BLUE, screen, SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return
        pygame.display.flip()
        clock.tick(60)

# Функция финального окна
def end_screen(score):
    while True:
        screen.fill((156, 180, 100))  # Зеленый фон
        draw_text(f"Игра закончена. Your Score: {score}", font, RED, screen, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 50)
        draw_text("Нажмите R, чтобы перезапустить, или ESC, чтобы выйти", font, BLUE, screen, SCREEN_WIDTH // 2 - 330, SCREEN_HEIGHT // 2 + 50)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    return True  # Перезапуск игры
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
        clock.tick(60)

# Настройка шрифта
font = pygame.font.Font(None, 36)

# Основной игровой цикл
current_level = 0
max_levels = len(levels)
score = 0
enemies_killed = 0  # Счетчик убитых врагов
clock = pygame.time.Clock()
FPS_1 = 3
FPS_2 = 30

# Список огоньков
projectiles = []

# Стартовое окно
start_screen()

while current_level < max_levels:
    player, coins, enemies, walls, flag = load_level(current_level)
    running = True

    while running:
        screen.fill((0, 255, 0))  # Зеленый фон (трава)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Обработка движения игрока
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player.move(0, -1, walls)
                elif event.key == K_DOWN:
                    player.move(0, 1, walls)
                elif event.key == K_LEFT:
                    player.move(-1, 0, walls)
                elif event.key == K_RIGHT:
                    player.move(1, 0, walls)
                elif event.key == K_SPACE:  # Стрельба огоньком
                    projectiles.append(Projectile(player.x, player.y, 1 if player.x < GRID_WIDTH // 2 else -1))

        # Обработка движения огоньков
        for projectile in projectiles[:]:  # Создаем копию списка для безопасного удаления
            projectile.move()
            if not (0 <= projectile.x < GRID_WIDTH):  # Если огонек вышел за пределы поля
                projectiles.remove(projectile)
            else:
                # Проверка столкновений с врагами
                for enemy in enemies[:]:
                    if projectile.x == enemy.x and projectile.y == enemy.y:
                        enemies.remove(enemy)  # Удаляем врага
                        enemies_killed += 1    # Увеличиваем счетчик убитых врагов
                        score += 20
                        enemy.respawn(walls)   # Возрождаем врага в случайной позиции
                        projectiles.remove(projectile)  # Удаляем огонек

        # Проверка столкновений с монетками
        for coin in coins[:]:  # Создаем копию списка для безопасного удаления
            if player.x == coin.x and player.y == coin.y and not coin.collected:
                coin.collected = True
                score += 10

        # Проверка столкновений с врагами
        for enemy in enemies:
            if player.x == enemy.x and player.y == enemy.y:
                running = False  # Конец уровня из-за поражения

        # Проверка столкновения с флагом
        if flag and player.x == flag.x and player.y == flag.y:
            show_level_result(screen, "Уровень пройден, поздравляем!", BLUE)
            current_level += 1  # Переход на следующий уровень
            break  # Выходим из игрового цикла

        # Движение врагов
        for enemy in enemies:
            enemy.move(walls)

        # Отрисовка игрового поля
        for row in range(len(walls)):
            for col in range(len(walls[row])):
                if walls[row][col]:  # Стена
                    screen.blit(wall_image, (col * TILE_SIZE, row * TILE_SIZE))
                else:
                    screen.blit(grass_image, (col * TILE_SIZE, row * TILE_SIZE))  # Трава

        # Отрисовка монеток
        for coin in coins:
            coin.draw(screen)

        # Отрисовка врагов
        for enemy in enemies:
            enemy.draw(screen)

        # Отрисовка флага
        if flag:
            flag.draw(screen)

        # Отрисовка игрока
        player.draw(screen)

        # Отрисовка огоньков
        for projectile in projectiles:
            projectile.draw(screen)

        # Отображение счета и убитых врагов
        draw_text(f"Score: {score}", font, BLUE, screen, 10, 10)
        draw_text(f"Enemies Killed: {enemies_killed}", font, RED, screen, 10, 40)

        pygame.display.flip()
        clock.tick(FPS_1)

    # Если игрок проиграл
    if not running:
        show_level_result(screen, "К сожалению, вы проиграли", RED)
        restart = end_screen(score)
        if restart:
            current_level = 0
            score = 0
            enemies_killed = 0
        else:
            break

# Финальный экран после завершения всех уровней
screen.fill((156, 180, 100))  # Зеленый фон
draw_text("Поздравляем! Вы прошли все уровни, ура!", font, BLUE, screen, 100, SCREEN_HEIGHT // 2 - 50)
draw_text(f"Финальный счёт: {score}", font, BLUE, screen, 100, SCREEN_HEIGHT // 2)
pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

