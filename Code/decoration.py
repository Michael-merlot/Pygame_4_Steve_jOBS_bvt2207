import pygame
from settings import vertical_tile_number, tile_size, screen_width
from support import import_folder
from random import choice, randint
from tiles import AnimatedTile, StaticTile


class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('../graphics/decoration/fon.png').convert()
        self.horizon = horizon

        # Растяяжка
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            surface.blit(self.top,(0, y))

class Clouds:
    def __init__(self, top, level_width):
        cloud_start = -screen_width
        cloud_tile_width = 192
        tile_x_amount = int((level_width + screen_width) / cloud_tile_width)
        self.cloud_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * cloud_tile_width + cloud_start
            y = top
            sprite = AnimatedTile(192, x, y, '../graphics/decoration/clouds')
            self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
