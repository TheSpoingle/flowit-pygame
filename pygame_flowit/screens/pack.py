import pygame
import typing

from pygame.event import Event

from flowit.packs import Pack
from flowit.level import Level
from flowit import storage
from pygame_flowit.screens import Button

from . import Screen


class PackScreen(Screen):
    def __init__(self, surface: pygame.Surface, pack: Pack, select_level_lambda, exit_lambda) -> None:
        super().__init__(surface)
        self.pack = pack
        self.select_level_lambda = select_level_lambda
        self.exit_lambda = exit_lambda

        self.font = pygame.font.SysFont('', int(40 * self.screen_scale))
        self.button_text_surfaces: list[pygame.Surface] = []
        self.generate_button_text_surfaces()
        self.scroll: float = 0.0

    def generate_button_text_surfaces(self):
        self.button_text_surfaces = []
        for level in self.pack.levels:
            self.button_text_surfaces.append(self.font.render(str(level.level_id), True, (128, 128, 128)))

    def get_level_icon(self, level: Level):
        storage_data = typing.cast(dict, storage.get(f"level_data.{level.pack_id}-{level.level_id}"))
        if storage_data == None:
            return "ui.pack.icon.default"
        elif level.solution != None and storage_data["best"] == len(level.solution):
            return "ui.pack.icon.completed_starred"
        else:
            return "ui.pack.icon.completed"

    def on_event(self, event: Event):
        super().on_event(event)
        if event.type == pygame.MOUSEWHEEL:
            self.scroll = max(min(self.scroll + event.precise_y * 30, 0), len(self.pack.levels) // 3 * -80 + 350)

    def on_button_pressed(self, button: Button):
        super().on_button_pressed(button)
        match button.category:
            case "level":
                self.select_level_lambda(self.pack, button.meta)
            case "exit":
                self.exit_lambda()

    def draw(self):
        super().draw()
        self.surface.fill((255, 255, 255))

        for level in self.pack.levels:
            button_group_start_pos = (
                ((level.level_id % 3) * (350 / 3) + 25) * self.screen_scale,
                ((level.level_id // 3) * 80  + 75 + self.scroll) * self.screen_scale
            )
            self.draw_button(
                self.get_level_icon(level),
                (int(button_group_start_pos[0]), int(button_group_start_pos[1]), int(50 * self.screen_scale), int(50 * self.screen_scale)),
                "level", level
            )
            button_text_surface = self.button_text_surfaces[level.level_id]
            self.surface.blit(button_text_surface, (button_group_start_pos[0] + (400 / 3 * 0.5 * self.screen_scale), button_group_start_pos[1] + (40 - button_text_surface.get_height() / 2) * self.screen_scale))
        
        self.draw_button("ui.pack.exit", (0, 0, int(64 * self.screen_scale), int(64 * self.screen_scale)), "exit")