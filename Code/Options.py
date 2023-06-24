import pygame
import sys
from settings import *

BLACK = (0, 0, 0)

def button_create(text, rect, inactive_color, active_color, action):
    font = pygame.font.Font(None, 40)
    button_rect = pygame.Rect(rect)
    text = font.render(text, True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    return [text, text_rect, button_rect, inactive_color, active_color, action, False]

def button_check(info, event):
    text, text_rect, rect, inactive_color, active_color, action, hover = info
    if event.type == pygame.MOUSEMOTION:
        info[-1] = rect.collidepoint(event.pos)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if hover and action:
            action

def button_draw(screen, info):
    text, text_rect, rect, inactive_color, active_color, action, hover = info
    if hover:
        color = active_color
    else:
        color = inactive_color
    pygame.draw.rect(screen, color, rect)
    screen.blit(text, text_rect)

class Options:
    def __init__(self, display_surface, game_menu, game):
        self.display_surface = display_surface
        self.game_menu = game_menu
        self.game = game
        self.menu_font = pygame.font.Font(None, 50)
        self.volume_level = self.game.level_bg_music.get_volume()

        #Загрузка изображения кнопки увеличения громкости
        self.volume_down_image = pygame.image.load('../graphics/image_menu/plus.png')
        #Загрузка изображения кнопки уменьшения громкости
        self.volume_up_image = pygame.image.load('../graphics/image_menu/minus.png')

        # Определение кнопок
        self.back_image = pygame.image.load('../graphics/image_menu/game.png')
        self.fullscreen_image = pygame.image.load('../graphics/image_menu/fullscreen.png')
        self.windowed_image = pygame.image.load('../graphics/image_menu/window.png')

        self.options_buttons = [
            {"image": self.fullscreen_image, "pos": (screen_width // 2 - 300, screen_height // 2 - 120),
             "call": self.fullscreen_mode},
            {"image": self.windowed_image, "pos": (screen_width // 2 + 300, screen_height // 2 - 120),
             "call": self.windowed_mode},
            {"image": self.volume_up_image, "pos": (screen_width // 2 - 200, screen_height // 2),
             "call": self.volume_up},
            {"image": self.volume_down_image, "pos": (screen_width // 2 + 200, screen_height // 2),
             "call": self.volume_down},
            {"image": self.back_image, "pos": (screen_width // 2, screen_height // 2 + 150),
             "call": self.go_back}
        ]

    def volume_up(self):
        # Уменьшаем громкость на 10%
        self.volume_level = min(1.0, self.volume_level - 0.1)
        self.game.level_bg_music.set_volume(self.volume_level)
        self.game.overworld_bg_music.set_volume(self.volume_level)
        self.game.menu_bg_music.set_volume(self.volume_level)
        print(f"Volume up, new volume level is: {self.volume_level}")

    def volume_down(self):
        # Увеличиваем громкость на 10%
        self.volume_level = max(0.0, self.volume_level + 0.1)
        self.game.level_bg_music.set_volume(self.volume_level)
        self.game.overworld_bg_music.set_volume(self.volume_level)
        self.game.menu_bg_music.set_volume(self.volume_level)
        print(f"Volume down, new volume level is: {self.volume_level}")

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in self.buttons:
                button_check(button, event)

    def draw(self):
        for button in self.buttons:
            button_draw(self.display_surface, button)

    def fullscreen_mode(self):
        pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    def windowed_mode(self):
        pygame.display.set_mode((screen_width, screen_height))

    def go_back(self):
        self.game_menu.go_to_main_menu()

    def run(self):
        # Отобразить фоновое изображение
        self.display_surface.blit(self.background_image, (0, 0))

        # Отобразить все кнопки
        for i, button in enumerate(self.buttons):
            if i == self.selected_button:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            self.display_surface.blit(button["image"], button["pos"])