import pygame
from settings import *
from random import *

class Raindrop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((3, 10))
        self.image.fill((175, 238, 238))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > screen_height:
            self.rect.y = -10