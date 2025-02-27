# Импортируем модули
import pygame
from pygame import *
import sys
import os
pygame.init()

# Инциализируем константы

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 25
LEVEL = 0
addnewflamerate = 20
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT ))
# Класс дракона

class Draacoon:
    global firerect, imagerect, Canvas
    up = False
    down = True
    velocity = 15

    def __init__(self):
        self.image = load_image("dragon_sheet8x2.png")
        self.image2 = AnimatedSprite(self.image, 8, 2, 50, 50)
        self.imagerect = self.image.get_rect()
        self.imagerect.right = WINDOW_WIDTH
        self.imagerect.top = WINDOW_HEIGHT / 2

    def update(self):

        if (self.imagerect.top < cactusrect.bottom):
            self.up = False
            self.down = True

        if (self.imagerect.bottom > firerect.top):
            self.up = True
            self.down = False

        if (self.down):
            self.imagerect.bottom += self.velocity

        if (self.up):
            self.imagerect.top -= self.velocity

        Canvas.blit(self.image, self.imagerect)

    def return_height(self):

        h = self.imagerect.top
        return h




class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]





#Класс огня
class Flame:
    flamespeed = 20

    def __init__(self):
        self.image = load_image('fireball.png')
        self.imagerect = self.image.get_rect()
        self.height = Dragon.return_height() + 20
        self.surface = pygame.transform.scale(self.image, (20, 20))
        self.imagerect = pygame.Rect(WINDOW_WIDTH - 106, self.height, 20, 20)

    def update(self):
        self.imagerect.left -= self.flamespeed

    def collision(self):
        if self.imagerect.left == 0:
            return True
        else:
            return False


# Класс самого марио
class Mario:
    global moveup, movedown, gravity, cactusrect, firerect
    speed = 10
    downspeed = 15
    def __init__(self):
        self.image = load_image('mario.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.topleft = (50, WINDOW_HEIGHT / 2)
        self.score = 0

    def update(self):

        if (moveup and (self.imagerect.top > cactusrect.bottom)):
            self.imagerect.top -= self.speed
            self.score += 1

        if (movedown and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom += self.downspeed
            self.score += 1

        if (gravity and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom += self.speed

# Окончание программы
def terminate():
    pygame.quit()
    sys.exit()


# Ждём, пока пользователь не начнет игру
def waitforkey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return


# Проверка, попал ли огонь в марио
def flamehitsmario(playerrect, flames):
    for f in flame_list:
        if playerrect.colliderect(f.imagerect):
            return True
        return False


def drawtext(text, font, surface, x, y):
    textobj = font.render(text, 1, WHITE)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Проверка уровня
def check_level(score):
    global WINDOW_HEIGHT, LEVEL, cactusrect, firerect
    if score in range(0, 250): #первый уровень до 250 набранных очков
        firerect.top = WINDOW_HEIGHT - 50
        cactusrect.bottom = 50
        LEVEL = 1
    elif score in range(250, 500): #второй уровень от 250 до 500 набранных очков
        firerect.top = WINDOW_HEIGHT - 100
        cactusrect.bottom = 100
        LEVEL = 2
    elif score in range(500, 750): #третий уровень от 500 до 750 набранных очков
        LEVEL = 3
        firerect.top = WINDOW_HEIGHT - 150
        cactusrect.bottom = 150
    elif score in range(750, 1000): #четвертый уровень от 750 до 1000 набранных очков
        LEVEL = 4
        firerect.top = WINDOW_HEIGHT - 200
        cactusrect.bottom = 200

# Функция загрузки изображений
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image




#Конец всех функций, начало основного кода

mainClock = pygame.time.Clock()
Canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('MARIOOOOO')

# Загружаем изображения

font = pygame.font.SysFont(None, 48)
scorefont = pygame.font.SysFont(None, 30)

fireimage = load_image('fire_bricks.png')
firerect = fireimage.get_rect()

cactusimage = load_image('cactus_bricks.png')
cactusrect = cactusimage.get_rect()

startimage = load_image('start.png')
startimagerect = startimage.get_rect()
startimagerect.centerx = WINDOW_WIDTH / 2
startimagerect.centery = WINDOW_HEIGHT / 2

endimage = load_image('end.png')
endimagerect = startimage.get_rect()
endimagerect.centerx = WINDOW_WIDTH / 2
endimagerect.centery = WINDOW_HEIGHT / 2

# Возвращаемся к стартовому окну

drawtext('Mario', font, Canvas, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
Canvas.blit(startimage, startimagerect)

pygame.display.update()
waitforkey()



topscore = 0
Dragon = Draacoon()

while True:

    flame_list = []
    player = Mario()
    moveup = movedown = gravity = False
    flameaddcounter = 0

    while True:
    # Основная проверка сочетания клавиш

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:

                if event.key == K_UP:
                    movedown = False
                    moveup = True
                    gravity = False

                if event.key == K_DOWN:
                    movedown = True
                    moveup = False
                    gravity = False

            if event.type == KEYUP:

                if event.key == K_UP:
                    moveup = False
                    gravity = True
                if event.key == K_DOWN:
                    movedown = False
                    gravity = True

                if event.key == K_ESCAPE:
                    terminate()

        flameaddcounter += 1
        check_level(player.score)

        if flameaddcounter == addnewflamerate:
            flameaddcounter = 0
            newflame = Flame()
            flame_list.append(newflame)

        for f in flame_list:
            Flame.update(f)

        for f in flame_list:
            if f.imagerect.left <= 0:
                flame_list.remove(f)

        player.update()
        Dragon.update()

        Canvas.fill(BLACK)
        Canvas.blit(fireimage, firerect)
        Canvas.blit(cactusimage, cactusrect)
        Canvas.blit(player.image, player.imagerect)
        Canvas.blit(Dragon.image, Dragon.imagerect)

        drawtext('Score : %s | Top score : %s | Level : %s' % (player.score, topscore, LEVEL), scorefont, Canvas, 350,
                 cactusrect.bottom + 10)

        for f in flame_list:
            Canvas.blit(f.surface, f.imagerect)

        if flamehitsmario(player.imagerect, flame_list):
            if player.score > topscore:
                topscore = player.score
            break

        if ((player.imagerect.top <= cactusrect.bottom) or (player.imagerect.bottom >= firerect.top)):
            if player.score > topscore:
                topscore = player.score
            break

        pygame.display.update()

        mainClock.tick(FPS)

    pygame.mixer.music.stop()
    Canvas.blit(endimage, endimagerect)
    pygame.display.update()
    waitforkey()