import pygame

from flowit import packs

from . import Screen
from . import Button


class PacksScreen(Screen):
    def __init__(self, surface, select_pack_lambda):
        super().__init__(surface)
        self.select_pack_lambda = select_pack_lambda
        self.font = pygame.font.SysFont('', int(60 * self.screen_scale))

        self.pack_text_surfaces: list[pygame.Surface] = []
        self.load_pack_text_surfaces()

    def load_pack_text_surfaces(self):
        for pack in packs.packs:
            pack_name = pack.name
            pack_text_surface = self.font.render(f"  {pack_name}  ", True, (255, 255, 255), (64, 64, 255))
            self.pack_text_surfaces.append(pack_text_surface)

    def on_button_pressed(self, button):
        super().on_button_pressed(button)
        self.select_pack_lambda(button.meta)

    def draw(self):
        self.surface.fill((255, 255, 255))
        for pack_id, pack_text_surface in enumerate(self.pack_text_surfaces):
            button_pos = (200 * self.screen_scale - pack_text_surface.get_width() / 2, (60 * self.screen_scale * pack_id))
            self.surface.blit(pack_text_surface, button_pos)
            self.buttons.append(Button(
                (int(button_pos[0]), int(button_pos[1]), pack_text_surface.get_width(), pack_text_surface.get_height()),
                "pack", packs.packs[pack_id]
            ))