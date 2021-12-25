import pygame
from sprites.text import Text

class Score(Text):
    def __init__(self):
        self.score = 0
        Text.__init__(self, str(self.score), 32,
                      pygame.color.Color(255, 0, 0), 100, 40)

    def update(self):
        Text.__init__(self, str(self.score), 32,
                      pygame.color.Color(255, 0, 0), 100, 40)
