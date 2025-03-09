import pygame
import sys
from pygame.locals import *
import random
import time


pygame.init()
pygame.mixer.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Мир Боба - Собери монетки!")

# Цвета
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (6, 72, 58)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 128, 0)
LIGHT_BLUE = (91, 146, 229)
# Размеры клетки
TILE_SIZE = 50

# Создание игрового поля
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# Загрузка фоновой музыки
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  


# Загрузка изображений
player_image = pygame.image.load("data/mario.png")
coin_image = pygame.image.load("data/star.png")
wall_image = pygame.image.load("data/preg.jpg")
wood_image = pygame.image.load("data/wood.jpg")
flag_image = pygame.image.load("data/flag.png")
fire_image = pygame.image.load("data/fireball.png")
question_image = pygame.image.load("data/question.png")
riddle_bg_img = pygame.image.load("data/zagadka.png")
fon_image = pygame.image.load("data/fon.jpg")

# Масштабирование изображений под размер клетки
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
coin_image = pygame.transform.scale(coin_image, (TILE_SIZE, TILE_SIZE))
wall_image = pygame.transform.scale(wall_image, (TILE_SIZE, TILE_SIZE))
wood_image = pygame.transform.scale(wood_image, (TILE_SIZE, TILE_SIZE))
flag_image = pygame.transform.scale(flag_image, (TILE_SIZE, TILE_SIZE))
fire_image = pygame.transform.scale(fire_image, (TILE_SIZE, TILE_SIZE))
question_image = pygame.transform.scale(question_image, (TILE_SIZE, TILE_SIZE))
riddle_bg_img = pygame.transform.scale(riddle_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
fon_image = pygame.transform.scale(fon_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Определение уровней
levels = [
    [
        'WWWWWWWWWWWWWWWW',
        'W   C   W  P  WW',
        'W      W W   W W',
        'WWW  W     E   W',
        'W   W    WW    W',
        'WW    C   I  W W',
        'W  E           W',
        'W   W      WWW W',
        'WCW  C WWWW    W',
        'W  E   W       W',
        'W     WW   C   FW',
        'WWWWWWWWWWWWWWWW',
    ],
    [
        'WWWWWWWWWWWWWWWW',
        'WWW E  C     EWW',
        'W    W   C    WW',
        'W   W     C  WIW',
        'W  E    W  WCW W',
        'W  E C       W W',
        'W    W C  WW   W',
        'W W  W W   C  WW',
        'W   C   WW     W',
        'W  E   WWWW  P W',
        'W     W W C WW FW',
        'WWWWWWWWWWWWWWWW',
    ],
    [
        'WWWWWWWWWWWWWWWW',
        'W  E       E   W',
        'W   W C W  C   W',
        'W   WWWWW     CW',
        'W  E      W    W',
        'WWE C      W  EW',
        'WWP     W    C W',
        'WW  W I W C    W',
        'W   C    W    WW',
        'W   E      W  WW',
        'W   WWW      C FW',
        'WWWWWWWWWWWWWWWW',
    ]
]

# Список загадок для каждого уровня
riddles = [
    {
        "question": "Какая птица носит название фрукта?",
        "answer": "киви"
    },
    {
        "question": "Каких камней не бывает в речке?",
        "answer": "сухих"
    },
    {
        "question": "Что не вместится даже в самую большую кастрюлю?",
        "answer": "её крышка"
    }
]

# Функция для отображения окна после уровня
def show_level_result(screen, message, color):
    screen.fill((156, 180, 100))  
    font = pygame.font.Font(None, 48)  
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()  
    time.sleep(2)   


# Функция для загрузки рекорда из файла
def load_record():
    try:
        with open("records.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                return int(lines[0].strip()), int(lines[1].strip())
    except FileNotFoundError:
        pass
    return 0, 0  # Возвращаем 0, если файл не существует


# Функция для сохранения рекорда в файл
def save_record(score, record, enemies_killed):
    with open("records.txt", "w") as file:
        file.write(f"{record}\n")  # Сохраняем рекорд
        file.write(f"{score}\n")  # Сохраняем последний результат
        file.write(f"{enemies_killed}\n")


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        for num in range(3, 6):  # Загружаем два кадра анимации
            img = pygame.image.load(f"data/boy_run_{num}.png")
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        self.index = 0
        self.animation_timer = 0
        self.is_moving = False

    def move(self, dx, dy, walls):
        new_rect = self.rect.move(dx * TILE_SIZE, dy * TILE_SIZE)
        if not any(new_rect.colliderect(wall.rect) for wall in walls):
            self.rect = new_rect
            self.is_moving = True
        else:
            self.is_moving = False

    def update(self):
        # Обновление анимации
        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= 3:  # Смена кадра каждые 10 тиков
                self.animation_timer = 0
                self.index = (self.index + 1) % len(self.images)  # Переключаем кадр
                self.image = self.images[self.index]
        else:
            self.image = self.images[0]  # Если игрок стоит, показываем первый кадр

# Класс монетки
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)


# Класс интеллектуальной клетки
class IntelligenceCell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = question_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Загрузка анимационных кадров
        self.frames = [
            pygame.transform.scale(pygame.image.load("data/enemy_run_1.png"), (TILE_SIZE, TILE_SIZE)),
            pygame.transform.scale(pygame.image.load("data/enemy_run_2.png"), (TILE_SIZE, TILE_SIZE)),
            pygame.transform.scale(pygame.image.load("data/enemy_run_3.png"), (TILE_SIZE, TILE_SIZE)),
            pygame.transform.scale(pygame.image.load("data/enemy_run_4.png"), (TILE_SIZE, TILE_SIZE)),
            pygame.transform.scale(pygame.image.load("data/enemy_run_5.png"), (TILE_SIZE, TILE_SIZE)),
            pygame.transform.scale(pygame.image.load("data/enemy_run_6.png"), (TILE_SIZE, TILE_SIZE)),
            pygame.transform.scale(pygame.image.load("data/enemy_run_7.png"), (TILE_SIZE, TILE_SIZE)),
            pygame.transform.scale(pygame.image.load("data/enemy_run_8.png"), (TILE_SIZE, TILE_SIZE)),
        ]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]  # Начальное изображение
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        self.direction = random.choice([-1, 1])  # Начальное направление движения
        self.animation_timer = 0  # Таймер для анимации
        self.facing_right = self.direction > 0  # Проверяем, движется ли враг вправо

    def update_animation(self):
        # Обновление анимации
        self.animation_timer += 1
        if self.animation_timer >= 3:  # Смена кадра каждые 3 тика
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            # Если враг движется влево, отражаем изображение
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def move(self, walls):
        new_rect = self.rect.move(self.direction * TILE_SIZE, 0)
        if not any(new_rect.colliderect(wall.rect) for wall in walls):
            self.rect = new_rect
        else:
            # При столкновении со стеной меняем направление
            self.direction *= -1
            self.facing_right = not self.facing_right  # Меняем ориентацию
            # Обновляем изображение сразу после разворота
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, walls):
        self.update_animation()  # Обновление анимации
        self.move(walls)  # Движение
# Класс огонька
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = fire_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        self.dx, self.dy = direction

    def update(self):
        self.rect = self.rect.move(self.dx * TILE_SIZE, self.dy * TILE_SIZE)


# Класс флага
class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = flag_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)


# Функция загрузки уровня
def load_level(level_index):
    level_data = levels[level_index]
    player_group = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    flag_group = pygame.sprite.Group()
    intelligence_cells = pygame.sprite.Group()

    for row_index, row in enumerate(level_data):
        for col_index, cell in enumerate(row):
            if cell == 'P':  # Игрок
                player = Player(col_index, row_index)
                player_group.add(player)
            elif cell == 'C':  # Монетка
                coins_group.add(Coin(col_index, row_index))
            elif cell == 'W':  # Стена
                wall = pygame.sprite.Sprite()
                wall.image = wall_image
                wall.rect = wall.image.get_rect()
                wall.rect.topleft = (col_index * TILE_SIZE, row_index * TILE_SIZE)
                walls.add(wall)
            elif cell == 'E':  # Враг
                enemies_group.add(Enemy(col_index, row_index))
            elif cell == 'F':  # Флаг
                flag_group.add(Flag(col_index, row_index))
            elif cell == 'I':  # Интеллектуальная клетка
                intelligence_cells.add(IntelligenceCell(col_index, row_index))

    return player_group, coins_group, enemies_group, walls, flag_group, intelligence_cells


# Функция для отображения загадки
def display_riddle(question):
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 32)
    color_inactive = pygame.Color('slategrey')
    color_active = pygame.Color('black')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

                # Отрисовка фона загадки

        screen.blit(riddle_bg_img, (0, 0))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        question_text = font.render(question, True, BLACK)
        screen.blit(question_text, (SCREEN_WIDTH // 2 - question_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

        pygame.display.flip()

    return text


# Функция для отображения стартового окна
def start_screen():
    screen.blit(fon_image, (0, 0))
    font = pygame.font.Font(None, 48)
    title_text = font.render("Добро пожаловать в игру Bob's World!", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    instruction_text = font.render("Нажмите SPACE, чтобы начать", True, RED)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    klavishi_text = font.render("Используйте стрелки для перемещения героя", True, BLACK)
    klavishi_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 100))
    hero_text = font.render("и клавиши W/A/S/D для стрельбы", True, BLUE)
    hero_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))

    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)
    screen.blit(klavishi_text, klavishi_rect)
    screen.blit(hero_text, hero_rect)
    pygame.display.flip()

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    waiting_for_start = False


# Вызов стартового окна перед основным циклом
start_screen()

# Основной игровой цикл
current_level = 0
max_levels = len(levels)
score = 0
enemies_killed = 0
clock = pygame.time.Clock()
FPS = 5

# Загрузка рекорда
record, _ = load_record()

while current_level < max_levels:
    player_group, coins_group, enemies_group, walls, flag_group, intelligence_cells = load_level(current_level)
    projectiles = pygame.sprite.Group()
    running = True

    while running:
        screen.fill((0, 255, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Обработка движения игрока
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player_group.sprites()[0].move(0, -1, walls)
                elif event.key == K_DOWN:
                    player_group.sprites()[0].move(0, 1, walls)
                elif event.key == K_LEFT:
                    player_group.sprites()[0].move(-1, 0, walls)
                elif event.key == K_RIGHT:
                    player_group.sprites()[0].move(1, 0, walls)

                # Обработка стрельбы
                elif event.key == K_w or event.key == K_UP:  # Стрельба вверх
                    projectiles.add(Projectile(player_group.sprites()[0].rect.x // TILE_SIZE,
                                               player_group.sprites()[0].rect.y // TILE_SIZE, (0, -1)))
                elif event.key == K_s or event.key == K_DOWN:  # Стрельба вниз
                    projectiles.add(Projectile(player_group.sprites()[0].rect.x // TILE_SIZE,
                                               player_group.sprites()[0].rect.y // TILE_SIZE, (0, 1)))
                elif event.key == K_a or event.key == K_LEFT:  # Стрельба влево
                    projectiles.add(Projectile(player_group.sprites()[0].rect.x // TILE_SIZE,
                                               player_group.sprites()[0].rect.y // TILE_SIZE, (-1, 0)))
                elif event.key == K_d or event.key == K_RIGHT:  # Стрельба вправо
                    projectiles.add(Projectile(player_group.sprites()[0].rect.x // TILE_SIZE,
                                               player_group.sprites()[0].rect.y // TILE_SIZE, (1, 0)))

        player_group.update()
        for enemy in enemies_group:
            enemy.update(walls)


        # Проверка столкновений с монетками
        for coin in pygame.sprite.groupcollide(player_group, coins_group, False, True).values():
            score += 15

        # Проверка столкновений с врагами
        if pygame.sprite.groupcollide(player_group, enemies_group, False, False):
            running = False  # Конец уровня из-за поражения

        # Проверка столкновений с флагом
        if pygame.sprite.groupcollide(player_group, flag_group, False, False):
            show_level_result(screen, "Уровень пройден, поздравляем!", BLUE)
            current_level += 1
            break

        # Проверка столкновений с интеллектуальной клеткой
        for cell in pygame.sprite.groupcollide(player_group, intelligence_cells, False, True).keys():
            riddle = riddles[current_level]
            correct = riddle["answer"]
            answer = display_riddle(riddle["question"])
            if answer.lower() == riddle["answer"]:
                score += 100
                print(f"Правильно! Ваш счет: {score}")
            else:
                print(f"Неправильно! Правильный ответ: {correct}")

        # Движение врагов
        for enemy in enemies_group:
            enemy.update(walls)

        # Обновление огоньков
        projectiles.update()

        # Проверка столкновений огоньков с врагами
        for projectile in pygame.sprite.groupcollide(projectiles, enemies_group, True, True).keys():
            enemies_killed += 1
            score += 30

        # Удаление огоньков за пределами поля
        for projectile in projectiles.copy():
            if not (0 <= projectile.rect.x < SCREEN_WIDTH and 0 <= projectile.rect.y < SCREEN_HEIGHT):
                projectiles.remove(projectile)

        # Отрисовка игрового поля
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                screen.blit(wood_image, (col * TILE_SIZE, row * TILE_SIZE))

        # Отрисовка стен
        walls.draw(screen)

        # Отрисовка всех спрайтов
        player_group.draw(screen)
        coins_group.draw(screen)
        enemies_group.draw(screen)
        flag_group.draw(screen)
        intelligence_cells.draw(screen)
        projectiles.draw(screen)

        # Отображение счета и убитых врагов
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счёт: {score}", True, BLUE)
        killed_text = font.render(f"Врагов убито: {enemies_killed}", True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(killed_text, (10, 40))

        pygame.display.flip()
        clock.tick(FPS)


    # Функция для отображения одного сообщения на экране
    def show_single_message(screen, message, color):
        screen.fill((156, 180, 100))  # Зеленый фон
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()  # Обновляем экран
        time.sleep(2)  # Ждем 2 секунды


    # Если игрок проиграл
    if not running:
        if score > record:
            record = score
        save_record(score, record, enemies_killed)

        messages = [
            (f"К сожалению, вы проиграли.", RED),
            (f"Финальный счёт: {score}", BLUE),
            (f"Врагов убито: {enemies_killed}", RED),
            (f"Нажмите R, чтобы перезапустить, или Esc, чтобы выйти", GREEN)
        ]

        for message, color in messages:
            show_single_message(screen, message, color)

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        current_level = 0
                        score = 0
                        enemies_killed = 0
                        waiting_for_input = False
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()



# Финальный экран после завершения всех уровней
screen.fill((156, 180, 100))  # Зеленый фон
font = pygame.font.Font(None, 48)
congrats_text = font.render("Ура! Вы прошли все уровни!", True, BLUE)
score_text = font.render(f"Финальный счёт: {score}, Врагов убито: {enemies_killed}", True, BLUE)
save_record(score, record, enemies_killed)
screen.blit(congrats_text, (100, SCREEN_HEIGHT // 2 - 50))
screen.blit(score_text, (100, SCREEN_HEIGHT // 2))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
