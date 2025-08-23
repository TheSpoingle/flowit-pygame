from . import map
from .level import Level
from .map import Coordinate


class Game():
    def __init__(self, level: Level) -> None:
        self.level = level
        self.start_map = level.map.copy()
        self.map = self.start_map.copy()
        self.moves = 0
    
    def move(self, position: Coordinate) -> map.MapSequence:
        maps = self.map.move(position)
        if len(maps) > 0:
            self.moves += 1
        return maps 

    def restart(self):
        self.map = self.start_map.copy()
        self.moves = 0