import pygame

from . import Screen
from . import Button

class MainScreen(Screen):
    def __init__(self, surface, play_lambda):
        super().__init__(surface)
        self.play_lambda = play_lambda


    def on_button_pressed(self, button):
        super().on_button_pressed(button)
        self.play_lambda()


    def draw(self):
        self.surface.fill((0, 0, 0))
        pygame.draw.rect(self.surface, (255, 128, 128), (0, 0, 20, 20))
        self.buttons.append(Button((0, 0, int(400 * self.screen_scale), int(500 * self.screen_scale)), "asdf"))