from . import packs
from . import storage

packs.load_packs()
storage.load_data()


# This function is for debugging purposes only
def test_levels():
    import time
    from .game import Game
    for pack in packs.packs:
        for level in pack.levels:
            if level.solution != None:
                test_game = Game(level)
                good = True
                for coordinate in level.solution:
                    if test_game.map.is_solved():
                        good = False
                    test_game.move(coordinate)
                if not test_game.map.is_solved():
                    good = False
                print(f"Level {level.pack_id}-{level.level_id}: {"Good" if good else "Bad"}")
                if not good:
                    print(level.solution)
                    time.sleep(1)
