import pygame
import sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI
from Code.Gamemenu import Gamemenu


class Game:
    def __init__(self):

        # Game attributes
        self.max_level = 5
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        # Music
        self.overworld_bg_music = pygame.mixer.Sound('../audio/overworld_music.mp3')
        self.level_bg_music = pygame.mixer.Sound('../audio/level_music.mp3')

        # World creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        pygame.mixer.music.play(loops=-1)

        # UI
        self.ui = UI(screen)

        # Game menu
        self.game_menu = Gamemenu(0, screen, self)
    def set_status_overworld(self):
        self.status = 'overworld'
        self.game_menu.music.stop()
        self.overworld_bg_music.play(loops=-1)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        pygame.mixer.music.stop()
        pygame.mixer.music.load('../audio/level_music.mp3')
        pygame.mixer.music.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)
        self.level_bg_music.stop()

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.current_health += amount

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops=-1)

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()


# Pygame setup
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('../Audio/level_music.mp3')
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.game_menu.handle_event(event)

    screen.fill('grey')
    game.run()
    game.game_menu.draw(screen)


    pygame.display.update()
    clock.tick(60)
