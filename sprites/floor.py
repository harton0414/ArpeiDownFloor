import pygame
import random


class Floor(pygame.sprite.Sprite):
    def __init__(self, floors, floor_imgs, screen_width, screen_height, floor_speedY):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(floor_imgs)
        self.rect = self.image.get_rect()  # set rectangle
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = screen_height + 50
        while pygame.sprite.spritecollide(self, floors, False):
            self.rect.x = random.randrange(0, screen_width - self.rect.width)
            self.rect.y = screen_height + 50
        self.speedy = floor_speedY

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
