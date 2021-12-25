# Game Logic Core
import math
import pygame
from sprites.score import Score
from sprites.player import Player
from sprites.floor import Floor


class Core:
    def __init__(self, settings, graphic_resource):
        self.settings = settings
        self.graphic_resource = graphic_resource

        self.floor_generate_interval = math.floor(
            settings.PLAYER_HEIGHT * 1.5) / abs(settings.FLOOR_SPEEDY)
        self.floor_generate_countdown = 0

        self.all_sprites = pygame.sprite.Group()  # 創建所有的sprites group
        self.floors = pygame.sprite.Group()

        self.score = Score()
        self.all_sprites.add(self.score)

        self.player = Player(graphic_resource.arpei_img,
                             settings.WIDTH, settings.HEIGHT, (255, 255, 255))
        self.all_sprites.add(self.player)

    def update(self):
        self.score.score += 1

        if self.floor_generate_countdown <= 0:
            self.floor_generate_countdown = self.floor_generate_interval
            self.add_floors()

        self.floor_generate_countdown -= 1

        self.all_sprites.update()  # 執行所有的項目的update
        self.__collide_check()
        if self.player.rect.y < 0:
            self.score.score = 0

    def add_floors(self):
        floor_imgs = self.graphic_resource.floor_imgs
        f = Floor(self.floors, floor_imgs, self.settings.WIDTH,
                  self.settings.HEIGHT, self.settings.FLOOR_SPEEDY)
        self.all_sprites.add(f)
        self.floors.add(f)

    def __collide_check(self):
        character = self.player
        floors = self.floors
        collided_floor = pygame.sprite.spritecollide(character, floors, False)

        if len(collided_floor) > 0:
            for _ in collided_floor:
                if character.rect.centerx < _.rect.left:
                    character.rect.right = _.rect.left
                if character.rect.centerx > _.rect.right:
                    character.rect.left = _.rect.right

                collide_rect = _.rect.clip(character)
                deltY = collide_rect.bottom - collide_rect.top
                character.rect.y -= deltY
                character.supported = True
        else:
            character.supported = False
