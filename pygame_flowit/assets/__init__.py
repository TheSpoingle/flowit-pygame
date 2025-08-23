import pygame
import typing

from ..config import assets_root_path, error_asset_path

asset_paths = {
    "error": "error.svg",
    "block": {
        "color": {
            "0": "block/color/block_color_0.svg",
            "r": "block/color/block_color_r.svg",
            "o": "block/color/block_color_o.svg",
            "g": "block/color/block_color_g.svg",
            "b": "block/color/block_color_b.svg",
            "d": "block/color/block_color_d.svg"
        },
        "modifier": {
            "0": "block/modifier/block_modifier_0.svg",
            "x": "block/modifier/block_modifier_x.svg",
            "F": {
                "r": "block/modifier/F/block_modifier_F_r.svg",
                "o": "block/modifier/F/block_modifier_F_o.svg",
                "g": "block/modifier/F/block_modifier_F_g.svg",
                "b": "block/modifier/F/block_modifier_F_b.svg",
                "d": "block/modifier/F/block_modifier_F_d.svg"
            },
            "U": {
                "r": "block/modifier/U/block_modifier_U_r.svg",
                "o": "block/modifier/U/block_modifier_U_o.svg",
                "g": "block/modifier/U/block_modifier_U_g.svg",
                "b": "block/modifier/U/block_modifier_U_b.svg",
                "d": "block/modifier/U/block_modifier_U_d.svg"
            },
            "R": {
                "r": "block/modifier/R/block_modifier_R_r.svg",
                "o": "block/modifier/R/block_modifier_R_o.svg",
                "g": "block/modifier/R/block_modifier_R_g.svg",
                "b": "block/modifier/R/block_modifier_R_b.svg",
                "d": "block/modifier/R/block_modifier_R_d.svg"
            },
            "D": {
                "r": "block/modifier/D/block_modifier_D_r.svg",
                "o": "block/modifier/D/block_modifier_D_o.svg",
                "g": "block/modifier/D/block_modifier_D_g.svg",
                "b": "block/modifier/D/block_modifier_D_b.svg",
                "d": "block/modifier/D/block_modifier_D_d.svg"
            },
            "L": {
                "r": "block/modifier/L/block_modifier_L_r.svg",
                "o": "block/modifier/L/block_modifier_L_o.svg",
                "g": "block/modifier/L/block_modifier_L_g.svg",
                "b": "block/modifier/L/block_modifier_L_b.svg",
                "d": "block/modifier/L/block_modifier_L_d.svg"
            },
            "B": {
                "r": "block/modifier/B/block_modifier_B_r.svg",
                "o": "block/modifier/B/block_modifier_B_o.svg",
                "g": "block/modifier/B/block_modifier_B_g.svg",
                "b": "block/modifier/B/block_modifier_B_b.svg",
                "d": "block/modifier/B/block_modifier_B_d.svg"
            },
            "w": {
                "r": "block/modifier/w/block_modifier_w_r.svg",
                "o": "block/modifier/w/block_modifier_w_o.svg",
                "g": "block/modifier/w/block_modifier_w_g.svg",
                "b": "block/modifier/w/block_modifier_w_b.svg",
                "d": "block/modifier/w/block_modifier_w_d.svg"
            },
            "x": {
                "r": "block/modifier/x/block_modifier_x_r.svg",
                "o": "block/modifier/x/block_modifier_x_o.svg",
                "g": "block/modifier/x/block_modifier_x_g.svg",
                "b": "block/modifier/x/block_modifier_x_b.svg",
                "d": "block/modifier/x/block_modifier_x_d.svg"
            },
            "a": {
                "r": "block/modifier/a/block_modifier_a_r.svg",
                "o": "block/modifier/a/block_modifier_a_o.svg",
                "g": "block/modifier/a/block_modifier_a_g.svg",
                "b": "block/modifier/a/block_modifier_a_b.svg",
                "d": "block/modifier/a/block_modifier_a_d.svg"
            },
            "s": {
                "r": "block/modifier/s/block_modifier_s_r.svg",
                "o": "block/modifier/s/block_modifier_s_o.svg",
                "g": "block/modifier/s/block_modifier_s_g.svg",
                "b": "block/modifier/s/block_modifier_s_b.svg",
                "d": "block/modifier/s/block_modifier_s_d.svg",
            },
            "r": "block/modifier/block_modifier_r.svg",
            "o": "block/modifier/block_modifier_o.svg",
            "g": "block/modifier/block_modifier_g.svg",
            "b": "block/modifier/block_modifier_b.svg",
            "d": "block/modifier/block_modifier_d.svg"
        }
    },
    "ui": {
        "game": {
            "back": "ui/game/ui_game_back.svg",
            "back_disabled": "ui/game/ui_game_back_disabled.svg",
            "forward": "ui/game/ui_game_forward.svg",
            "forward_disabled": "ui/game/ui_game_forward_disabled.svg",
            "star": "ui/game/ui_game_star.svg",
            "restart": "ui/game/ui_game_restart.svg",
            "exit": "ui/game/ui_game_exit.svg"
        },
        "pack": {
            "icon": {
                "default": "ui/pack/icon/pack_level_icon.svg",
                "completed": "ui/pack/icon/pack_level_icon_completed.svg",
                "completed_starred": "ui/pack/icon/pack_level_icon_completed_starred.svg"
            },
            "exit": "ui/pack/ui_pack_exit.png"
        }
    }
}

assets = {}


def load_assets_recursive(src_dict: dict, dest_dict: dict):
    for key in src_dict:
        value = src_dict[key]
        if isinstance(value, dict):
            dest_dict[key] = {}
            load_assets_recursive(value, dest_dict[key])
        else:
            print("\033[2K\rLoading asset at " + value, end="")
            try:
                image_surface = pygame.image.load(assets_root_path + value)
                dest_dict[key] = image_surface
            except:
                print("\033[2K\rFailed to load asset at path " + value)
                dest_dict[key] = pygame.image.load(assets_root_path + error_asset_path)

def load_assets():
    print("Loading assets")
    load_assets_recursive(asset_paths, assets)
    print("\033[2K\rLoaded all assets")

def get_asset(path: str, size: tuple[int, int] | None = None) -> pygame.Surface:
    try:
        d = assets
        for part in path.split("."):
            d = d[part]
        
        asset = typing.cast(pygame.Surface, d)
        if size == None:
            return asset
        else:
            return pygame.transform.scale(asset, size)
    except:
        print(f"Invalid asset at path {path}")
        if size == None:
            return assets["error"]
        else:
            return pygame.transform.scale(assets["error"], size)