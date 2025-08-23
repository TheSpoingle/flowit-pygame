import pygame

from .. import assets

screen_scale: float = 2.0


class Button():
    def __init__(self, rect: tuple[int, int, int, int], category: str = "", meta = None):
        self.rect = rect
        self.category = category
        self.meta = meta
    

    def clicked_inside(self, pos: tuple[int, int]) -> bool:
        return\
            pos[0] >= self.rect[0] and \
            pos[1] >= self.rect[1] and \
            pos[0] <= self.rect[0] + self.rect[2] and \
            pos[1] <= self.rect[1] + self.rect[3]


class Screen():
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface        
        self.screen_scale = screen_scale
        self.buttons: list[Button] = []


    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                for button in reversed(self.buttons):
                    if button.clicked_inside(event.pos):
                        self.on_button_pressed(button)
                        break


    def on_button_pressed(self, button: Button):
        pass


    def draw_button(self, asset_path: str = "", rect: tuple[int, int, int, int] = (0, 0, 0, 0), category: str = "", meta = None):
        self.surface.blit(assets.get_asset(asset_path, (rect[2], rect[3])), (rect[0], rect[1]))
        self.buttons.append(Button(rect, category, meta))
    

    def draw(self):
        self.buttons = []