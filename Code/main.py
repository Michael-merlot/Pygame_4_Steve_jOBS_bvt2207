import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI
from Gamemenu import Gamemenu
from Options import Options
from tutorial import Tutorial

class Game:
    def __init__(self, screen):
        self.screen = screen

        # Игровые атрибуты
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        # Музыка
        self.level_bg_music = pygame.mixer.Sound('../audio/level_music.mp3')
        self.overworld_bg_music = pygame.mixer.Sound('../audio/overworld_music.mp3')
        self.menu_bg_music = pygame.mixer.Sound('../audio/menu_music.mp3')

        self.game_menu = Gamemenu(0, self.screen, self)
        self.tutorial_shown = False
        self.tutorial = None

        # Установка начальной громкости
        self.volume_level = 1.0
        self.level_bg_music.set_volume(self.volume_level)
        self.overworld_bg_music.set_volume(self.volume_level)
        self.options = Options(self.screen, self.game_menu, self)

        # Создание мира
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'menu'  # начинаем с меню
        self.game_menu = Gamemenu(0, screen, self)
        self.overworld_bg_music.play(loops=-1)

        # Пользовательский интерфейс
        self.ui = UI(screen)

    def set_status_overworld(self):
        self.status = 'overworld'

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops=-1)

        if not self.tutorial_shown:
            self.tutorial = Tutorial(self.screen)
            self.tutorial_shown = True
        else:
            self.tutorial = None

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
        if self.status == 'menu':
            self.game_menu.draw(screen)
        elif self.status == 'overworld':
            self.overworld.run()
        elif self.status == 'level':
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()

            if not self.tutorial_shown:
                self.tutorial.run()


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.status != 'menu':
                    game.status = 'menu'
                    game.level_bg_music.stop()
                    game.overworld_bg_music.stop()
                    if not pygame.mixer.get_busy():
                        game.menu_bg_music.play()

        if game.status == 'menu':
            game.game_menu.handle_event(event)
            game.tutorial = None

    if game.status == 'menu':
        # Остановить другую музыку и воспроизведите музыку меню
        game.level_bg_music.stop()
        game.overworld_bg_music.stop()
        if not pygame.mixer.get_busy():
            game.menu_bg_music.play()
    elif game.status == 'overworld':
        # Остановить другую музыку и воспроизведите музыку overworld
        game.menu_bg_music.stop()
        game.level_bg_music.stop()
        if not pygame.mixer.get_busy():
            game.overworld_bg_music.play()
    elif game.status == 'level' and game.tutorial is not None:
        game.tutorial.handle_event(event)
        # Остановить другую музыку и воспроизведите музыку уровня
        game.menu_bg_music.stop()
        game.overworld_bg_music.stop()
        if not pygame.mixer.get_busy():
            game.level_bg_music.play()

    screen.fill('grey')
    game.run()

    if game.tutorial is not None:
        game.tutorial.handle_event(event)
        game.tutorial.draw()

    pygame.display.update()
    clock.tick(60)