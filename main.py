from math import floor
import pygame
import os
import random

WIDTH = 500
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
TITLE = "阿沛下樓梯"

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


def new_floor():
    r = Floor()
    all_sprites.add(r)
    floors.add(r)

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


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(floor_imgs)
        self.rect = self.image.get_rect()  # set rectangle
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(650, 700)
        self.speedy = -5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(650, 900)
            self.speedy = -5


all_sprites = pygame.sprite.Group()  # 創建所有的sprites group
floors = pygame.sprite.Group()
arpei = Arpei()
all_sprites.add(arpei)
for i in range(4):
    new_floor()

running = True
while running:
    clock.tick(FPS)  # 每一秒最多執行幾次

    # 取得input
    for event in pygame.event.get():  # 取得所有事件
        if event.type == pygame.QUIT:
            running = False

    # 更新遊戲
    all_sprites.update()  # 執行所有的項目的update

    # show
    screen.fill(WHITE)
    all_sprites.draw(screen)  # 將sprites畫在screen上
    pygame.display.update()  # 更新display

# 離開
pygame.quit()
