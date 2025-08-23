import pygame
import time
import typing

from flowit.packs import Pack
from flowit.game import Game
from flowit.level import Level
from flowit import storage

from . import screens
from .screens import Screen
from .screens.main import MainScreen
from .screens.game import GameScreen
from .screens.packs import PacksScreen
from .screens.pack import PackScreen
from . import assets

display_surface: pygame.Surface
screen: Screen


def on_main_screen_play():
    global screen
    screen = create_packs_screen()

def on_packs_screen_pack_selected(pack: Pack):
    global screen
    screen = create_pack_screen(pack)

def on_pack_screen_level_selected(pack: Pack, level: Level):
    global screen
    screen = create_game_screen(pack, level)

def on_pack_screen_exit():
    global screen
    screen = create_packs_screen()

def on_game_screen_exit():
    global screen
    screen = create_pack_screen(typing.cast(PackScreen, screen).pack)

def on_game_screen_navigate(direction: int):
    global screen
    screen = typing.cast(GameScreen, screen)
    level: Level = screen.game.level
    new_level_id = level.level_id + direction
    if new_level_id == -1 or new_level_id >= len(screen.pack.levels):
        return
    new_level = screen.pack.levels[new_level_id]
    screen = create_game_screen(screen.pack, new_level)

def create_main_screen() -> MainScreen:
    return MainScreen(display_surface, on_main_screen_play)

def create_packs_screen() -> PacksScreen:
    return PacksScreen(display_surface, on_packs_screen_pack_selected)

def create_pack_screen(pack: Pack) -> PackScreen:
    return PackScreen(display_surface, pack, on_pack_screen_level_selected, on_pack_screen_exit)

def create_game_screen(pack: Pack, level: Level) -> GameScreen:
    global screen
    return GameScreen(display_surface, pack, Game(level), on_game_screen_exit, on_game_screen_navigate)

def run():
    global display_surface
    global screen

    assets.load_assets()

    pygame.init()
    pygame.font.init()

    display_surface = pygame.display.set_mode((400 * screens.screen_scale, 500 * screens.screen_scale), pygame.HWSURFACE | pygame.DOUBLEBUF)

    clock = pygame.time.Clock()
    last_draw = time.time()

    screen = create_packs_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            screen.on_event(event)
        
        pygame.display.set_caption(str(int(1.0 / (time.time() - last_draw))))
        last_draw = time.time()
        screen.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    storage.save_data()