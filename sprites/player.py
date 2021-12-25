import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, screen_width, screen_height, colorkey):
        pygame.sprite.Sprite.__init__(self)  # initialize
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = image
        self.image.set_colorkey(colorkey)

        self.image_l = self.image
        self.image_r = pygame.transform.flip(self.image, True, False)
        

        self.rect = self.image.get_rect()  # set rectangle
        self.rect.centerx = screen_width / 2
        self.rect.centery = screen_height / 4
        self.speedx = 5

        self.supported = False                  # Need Collide check with Floor
        self.gravity = 0.6                      # Y axis acceleration
        self.speedy = 0
        
        self.dead = False



    def update(self):
        key_pressed = pygame.key.get_pressed()  # get the pressed key

        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
            self.image = self.image_r
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
            self.image = self.image_l
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < 0:
            self.rect.left = 0

        if self.supported:
            self.speedy = 0
        else:
            self.speedy += self.gravity
        self.rect.y += self.speedy

        if self.rect.y > self.screen_height:
            self.rect.y = -10
            self.speedy = 0
