import pygame
import sys
from settings import *
from Options import Options


class Gamemenu:
    def __init__(self, status, screen, game):
        self.display_surface = screen
        self.current_menu = status
        self.menu_font = pygame.font.Font(None, 50)
        self.game = game
        self.options = Options(screen, self, game)

        self.background_image = pygame.image.load('../graphics/image_menu/menu.png')
        self.levels_image = pygame.image.load('../graphics/image_menu/game.png')
        self.settings_image = pygame.image.load('../graphics/image_menu/game.png')
        self.exit_image = pygame.image.load('../graphics/image_menu/game.png')
        self.toggle_fullscreen_image = pygame.image.load('../graphics/image_menu/game.png')
        self.back_image = pygame.image.load('../graphics/image_menu/game.png')

        self.main_menu_buttons = [
            {"image": self.levels_image, "pos": (screen_width // 2, screen_height // 2 - 150),
             "call": self.go_to_levels},
            {"image": self.settings_image, "pos": (screen_width // 2, screen_height // 2), "call": self.go_to_settings},
            {"image": self.exit_image, "pos": (screen_width // 2, screen_height // 2 + 150), "call": sys.exit}
        ]
        self.settings_menu_buttons = [
            {"image": self.toggle_fullscreen_image, "pos": (screen_width // 2, screen_height // 2 - 25),
             "call": self.toggle_fullscreen},
            {"image": self.back_image, "pos": (screen_width // 2, screen_height // 2 + 25),
             "call": self.go_to_main_menu}
        ]

        self.buttons = self.main_menu_buttons
        self.selected_button = 0
        self.options = Options(self.display_surface, self, game)

    def go_to_settings(self):
        self.buttons = self.options.options_buttons
        self.selected_button = 0

    def go_to_main_menu(self):
        self.buttons = self.main_menu_buttons
        self.selected_button = 0

    def toggle_fullscreen(self):
        self.options.toggle_fullscreen()

    def draw(self, surface):
        surface.blit(self.background_image, (0, 0))

        for i, button in enumerate(self.buttons):
            if i == self.selected_button:
                # Увеличиваем выбранное изображение на 10%
                scaled_image = pygame.transform.scale(button["image"], (
                int(button["image"].get_width() * 1.1), int(button["image"].get_height() * 1.1)))
                image_rect = scaled_image.get_rect(center=button["pos"])
                surface.blit(scaled_image, image_rect)
            else:
                image_rect = button["image"].get_rect(center=button["pos"])
                surface.blit(button["image"], image_rect)

    # Новый метод для обработки событий
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.selected_button = max(0, self.selected_button - 1)
            elif event.key == pygame.K_s:
                self.selected_button = min(len(self.buttons) - 1, self.selected_button + 1)
            elif event.key == pygame.K_SPACE:
                self.buttons[self.selected_button]["call"]()

    def go_to_levels(self):
        self.game.set_status_overworld()

    def run(self):
        pass
