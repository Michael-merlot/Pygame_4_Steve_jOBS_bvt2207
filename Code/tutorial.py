import pygame
class Tutorial:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.texts = [
            "Добро пожаловать в обучение!",
            "Используйте клавиши A, D для движения",
            "Нажмите Space, чтобы прыгать",
            "Для выхода в Главное меню - нажмите ESC",
            "Если вам мешает противник, прыгайте на его голову!",
            "Желаю вам удачи!"
        ]
        self.current_text = 0
        self.start_time = pygame.time.get_ticks()

    def draw(self):
        if self.current_text < len(self.texts):
            text = self.font.render(self.texts[self.current_text], True, (255, 255, 255))
            self.screen.blit(text, (100, 100))

        if pygame.time.get_ticks() - self.start_time >= 4000:
            self.current_text += 1
            self.start_time = pygame.time.get_ticks()  # обновляем время начала показа следующего сообщения

    def next(self):
        if self.current_text < len(self.texts) - 1:
            self.current_text += 1

    def run(self):
        if self.current_text < len(self.texts):
            self.draw()
