import pygame
import time
import typing

from flowit.game import Game
from flowit.map import Map, Coordinate, Color, Modifier
from flowit.packs import Pack
from flowit import storage

from pygame_flowit import assets

from . import Screen
from . import Button

background_color = (255, 255, 255)
nav_bar_color = (223, 223, 223)
map_switch_delay = 0.025


class GameScreen(Screen):
    def __init__(self, surface: pygame.Surface, pack: Pack, game: Game, exit_lambda, navigate_lambda) -> None:
        super().__init__(surface)
        self.pack = pack
        self.game = game
        self.exit_lambda = exit_lambda
        self.navigate_lambda = navigate_lambda

        self.last_map_switch: float = time.time()
        self.map_queue: list[Map] = []
        self.map: Map = self.game.map

        self.best_moves: int = typing.cast(int, storage.get(f"level_data.{self.game.level.pack_id}-{self.game.level.level_id}.best"))

        self.update_text_queued = True
        self.text_surfaces = []
        self.font: pygame.font.Font = pygame.font.SysFont('', int(30 * self.screen_scale))

    def save_best(self):
        storage.set(f"level_data.{self.game.level.pack_id}-{self.game.level.level_id}.best", self.game.moves)

    def restart(self):
        self.game.restart()
        self.map_queue = []
        self.map = self.game.map
        self.update_text_queued = True

    def on_button_pressed(self, button: Button):
        super().on_button_pressed(button)

        match button.category:
            case "block":
                if len(self.map_queue) > 0:
                    self.map_queue = []
                self.map = self.map.copy()
                for map in self.game.move(typing.cast(Coordinate, button.meta)):
                    self.map_queue.append(map)
                self.update_text_queued = True
            case "exit":
                self.exit_lambda()
            case "restart":
                self.restart()
            case "navigate":
                self.navigate_lambda(button.meta)

    def update_text_surfaces(self):
        lines = [
            f"Current: {self.game.moves}",
            f"Best: {"-" if self.best_moves == None else self.best_moves}"
        ]
        if self.game.level.solution:
            lines.append(f"Optimal: {len(self.game.level.solution)}")

        self.text_surfaces = []
        for line in lines:
            self.text_surfaces.append(self.font.render(line, True, (0, 0, 0)))
        self.update_text_queued = False

    def draw(self):
        super().draw()
        self.surface.fill(background_color)

        # Update map
        if len(self.map_queue) > 0:
            if time.time() - self.last_map_switch >= map_switch_delay:
                self.last_map_switch = time.time()
                self.map = self.map_queue.pop(0)
            if len(self.map_queue) == 0:
                self.map_switch_fast_forward = False
        
        # Navigation bar
        nav_bar_height = 75 * self.screen_scale
        pygame.draw.rect(self.surface, nav_bar_color, (0, 0, 400 * self.screen_scale, nav_bar_height))
        nav_bar_button_size = 50 * self.screen_scale
        self.draw_button(
            "ui.game.back" if self.game.level.level_id > 0 else "ui.game.back_disabled",
            (0, int((nav_bar_height - nav_bar_button_size) / 2), int(nav_bar_button_size), int(nav_bar_button_size)),
            "navigate", -1
        )
        self.draw_button(
            "ui.game.restart",
            (int(nav_bar_button_size), int((nav_bar_height - nav_bar_button_size) / 2), int(nav_bar_button_size), int(nav_bar_button_size)),
            "restart"
        )
        self.draw_button(
            "ui.game.exit",
            (int(400 * self.screen_scale - nav_bar_button_size * 2), int((nav_bar_height - nav_bar_button_size) / 2), int(nav_bar_button_size), int(nav_bar_button_size)),
            "exit"
        )
        self.draw_button(
            "ui.game.forward" if self.game.level.level_id < len(self.pack.levels) - 1 else "ui.game.forward_disabled",
            (int(400 * self.screen_scale - nav_bar_button_size), int((nav_bar_height - nav_bar_button_size) / 2), int(nav_bar_button_size), int(nav_bar_button_size)),
            "navigate", 1
        )

        if self.update_text_queued:
            self.update_text_surfaces()

        for i, text_surface in enumerate(self.text_surfaces):
            self.surface.blit(text_surface, (200 * self.screen_scale - text_surface.get_width() / 2, 18.75 * self.screen_scale * (i + 0.5)))

        map_size = self.game.level.map.size
        grid_size = 400 * self.screen_scale / max(map_size[0], map_size[1])
        block_size = grid_size * 0.95
        block_offset = ((grid_size - block_size) / 2, (grid_size - block_size) / 2 + 100 * self.screen_scale)
        min_is_x = map_size[0] < map_size[1]
        if min_is_x:
            block_offset = (block_offset[0] + (400 * self.screen_scale - grid_size * map_size[0]) / 2, block_offset[1])
        else:
            block_offset = (block_offset[0], block_offset[1] + (400 * self.screen_scale - grid_size * map_size[1]) / 2)

        for x in range(map_size[0]):
            for y in range(map_size[1]):
                block = self.map.get_block(Coordinate(x, y))
                
                if block.color != Color.NONE:
                    block_pos = (int(grid_size * x + block_offset[0]), int(grid_size * y + block_offset[1]))
                    back_asset_path = f"block.color.{block.color.value}"
                    self.surface.blit(assets.get_asset(back_asset_path, (int(block_size + 1), int(block_size + 1))), block_pos)

                    fore_asset_path = ""
                    match block.modifier:
                        case Modifier.NONE | Modifier.DISABLED:
                            fore_asset_path = ""
                        case Modifier.RED | Modifier.ORANGE | Modifier.GREEN | Modifier.BLUE | Modifier.DARK:
                            fore_asset_path = f"block.modifier.{block.modifier.value}"
                        case _:
                            fore_asset_path = f"block.modifier.{block.modifier.value}.{block.color.value}"
                    if fore_asset_path != "":
                        self.surface.blit(assets.get_asset(fore_asset_path, (int(block_size + 1), int(block_size + 1))), block_pos)
                    
                    self.buttons.append(Button((int(block_pos[0]), int(block_pos[1]), int(block_size + 1), int(block_size + 1)), "block", Coordinate(x, y)))
        
        if len(self.map_queue) == 0:
            # if self.game.check_win():
            if self.game.map.is_solved():
                if self.best_moves == None or self.game.moves < self.best_moves:
                    self.best_moves = self.game.moves
                    self.save_best()
                # elif self.game.moves < self.best_moves:
                #     self.best_moves = self.game.moves
                #     self.save_best()
                self.restart()