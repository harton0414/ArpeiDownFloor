from math import floor
import math
import pygame
import os
import random

# 雜七雜八參數設定
WIDTH = 500
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
TITLE = "阿沛下樓梯"
FLOOR_SPEEDY = -5

# 初始化
pygame.init()

# 視窗相關
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 創建視窗
pygame.display.set_caption(TITLE)  # 設定標題
clock = pygame.time.Clock()

# 圖片相關
arpei_left_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "arpei.png")).convert(), (50, 60))
arpei_right_img = pygame.transform.flip(arpei_left_img, True, False)
floor_imgs = []
for i in range(2):
    floor_imgs.append(pygame.image.load(
        os.path.join("img", f"floor{i}.png")).convert())

# 音效相關
pygame.mixer.init()  # 處理聲音的
pygame.mixer.music.load(os.path.join("sound", "flogs_loop.mp3"))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # 播放音效，-1表示無限次播放

# floor test


def new_floor():
    r = Floor()
    all_sprites.add(r)
    floors.add(r)

# collide


def collide_check():
    collided_floor = pygame.sprite.spritecollide(arpei, floors, False)
    if len(collided_floor) > 0:
        for _ in collided_floor:
            if arpei.rect.centerx < _.rect.left:
                arpei.rect.right = _.rect.left
            if arpei.rect.centerx > _.rect.right:
                arpei.rect.left = _.rect.right

            collide_rect = _.rect.clip(arpei)
            deltY = collide_rect.bottom - collide_rect.top
            arpei.rect.y -= deltY
            arpei.supported = True
    else:
        arpei.supported = False


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, 1, color)
        self.image = pygame.Surface((width, height))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])
        self.rect = self.textSurf.get_rect()


score = 0


class Score(Text):
    def __init__(self):
        Text.__init__(self, str(score), 32, pygame.color.Color(255, 0, 0), 100, 40)
    def update(self):
        Text.__init__(self, str(score), 32, pygame.color.Color(255, 0, 0), 100, 40)        

# 阿沛


class Arpei(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # initialize
        self.image = arpei_left_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()  # set rectangle
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 4
        self.speedx = 5

        self.supported = False                  # Need Collide check with Floor
        self.gravity = 0.6                      # Y axis acceleration
        self.speedy = 0

    def update(self):
        key_pressed = pygame.key.get_pressed()  # get the pressed key

        if key_pressed[pygame.K_RIGHT]:
            self.image = arpei_right_img
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.image = arpei_left_img
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.supported:
            self.speedy = 0
        else:
            self.speedy += self.gravity
        self.rect.y += self.speedy

        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.speedy = 0


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(floor_imgs)
        self.rect = self.image.get_rect()  # set rectangle
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = HEIGHT + 50
        while pygame.sprite.spritecollide(self, floors, False):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = HEIGHT + 50
        self.speedy = FLOOR_SPEEDY

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()  # 創建所有的sprites group
floors = pygame.sprite.Group()
arpei = Arpei()
all_sprites.add(arpei)
sc = Score()
all_sprites.add(sc)

running = True
floor_i = 0
floor_interval = math.floor(arpei.rect.height * 1.5) / abs(FLOOR_SPEEDY)
while running:
    clock.tick(FPS)  # 每一秒最多執行幾次

    # 取得input
    for event in pygame.event.get():  # 取得所有事件
        if event.type == pygame.QUIT:
            running = False

    # 新增地板
    floor_i += 1
    if floor_i == floor_interval:
        new_floor()
        floor_i = 0

    # 更新遊戲
    score+=1
    all_sprites.update()  # 執行所有的項目的update
    collide_check()

    # show
    screen.fill(WHITE)
    all_sprites.draw(screen)  # 將sprites畫在screen上
    pygame.display.update()  # 更新display

# 離開
pygame.quit()
exit()
