from typing import TypeAlias
from dataclasses import dataclass

from .map import Map, Coordinate, Color, Modifier, Block

coordinate_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

Solution: TypeAlias = list[Coordinate]


class LevelError(Exception):
    pass

class CreateLevelError(LevelError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

@dataclass
class Level:
    pack_id: int
    level_id: int
    number: int
    solution: Solution | None
    author: str
    map: Map

    @staticmethod
    def from_dict(data: dict, pack_id: int, level_id: int):
        # List of all properties needed to load a level from a dict
        property_data: list[tuple[str, type, bool]] = [
            ("number",   int, True  ),
            ("solution", str, False ),
            ("author",   str, False ),
            ("color",    str, True  ),
            ("modifier", str, True  )
        ]

        # Load properties
        properties = {}
        for key, t, required in property_data:
            if key not in data:
                # Error if required
                if required:
                    raise CreateLevelError(message=f"Required key {key} not in level data")
                # Otherise leave blank
                properties[key] = None
            else:
                # Check if key is right data type, error if not
                if not isinstance(data[key], t):
                    raise CreateLevelError(message=f"Invalid type for key {key}. Got {type(data[key]).__name__} but expected {t.__name__}.")
                # Continue if correct data type
                properties[key] = data[key]
        
        number: int = properties["number"]
        solution_str: str = properties["solution"]
        author: str = properties["author"]
        color: str = properties["color"]
        modifier: str = properties["modifier"]

        # Load solution from coordinate list of [str A-Z, int]
        solution: Solution | None
        if solution_str != None:
            # If a solution was provided, process it below
            solution_arr = solution_str.split(",")
            solution = []
            for coordinate_str in solution_arr:
                if len(coordinate_str) < 2:
                    raise CreateLevelError(message=f"Coordinate {coordinate_str} does not fit format - is not a 2 or more character string.")
                x_char = coordinate_str[0]
                if x_char not in coordinate_letters:
                    raise CreateLevelError(message=f"Coordinate x string value \"{x_char}\" does not fit format - x is not a valid A-Z character.")
                x = coordinate_letters.index(x_char)
                try:
                    y = int(coordinate_str[1:]) - 1
                except ValueError:
                    raise CreateLevelError(message=f"Coordinate {coordinate_str} does not fit format - y is not an integer.")
                solution.append(Coordinate(x, y))
        else:
            solution = None

        # Load colors and modifiers from string space-separated row groups
        colors = color.split(" ")
        modifiers = modifier.split(" ")
        if [len(row) for row in colors] != [len(row) for row in modifiers]:
            raise CreateLevelError(message="Lengths of color and modifier do not match.")
        if len(colors) == 0:
            raise CreateLevelError(message="Map is too small - there are no columns.")
        if len(colors[0]) == 0:
            raise CreateLevelError(message="Map is too small - there are no rows.")
        
        # Currently Unused
        # # Crop map to remove empty borders (leftover from preset sizes from the orginal flowit game)
        # cropped_width = 0
        # cropped_height = 0
        # for row in range(len(colors)):
        #     row_has_content = False
        #     for col in range(cropped_width, len(colors[row])):
        #         color = colors[row][col]
        #         if color != Color.NONE.value:
        #             cropped_width = max(cropped_width, col)
        #             row_has_content = True
        #     if row_has_content:
        #         cropped_height = row

        # map_data: list[list[Block]] = []
        # for row in range(cropped_height + 1):
        #     map_data.append([])
        #     for col in range(cropped_width + 1):
        #         try:
        #             c = Color(colors[row][col])
        #         except ValueError:
        #             raise CreateLevelError(message=f"Color char {colors[row][col]} is not valid.")
        #         try:
        #             m = Modifier(modifiers[row][col])
        #         except ValueError:
        #             raise CreateLevelError(message=f"Modifier char {modifiers[row][col]} is not valid.")
        #         map_data[row].append(Block(color=c, modifier=m))

        # Create the map from the colors and modifiers
        map_data: list[list[Block]] = []
        for row in range(len(colors)):
            map_data.append([])
            for col in range(len(colors[row])):
                try:
                    c = Color(colors[row][col])
                except ValueError:
                    raise CreateLevelError(message=f"Color char {colors[row][col]} is not valid.")
                try:
                    m = Modifier(modifiers[row][col])
                except ValueError:
                    raise CreateLevelError(message=f"Modifier char {modifiers[row][col]} is not valid.")
                map_data[row].append(Block(color=c, modifier=m))
        
        return Level(pack_id, level_id, number, solution, author, Map(map_data))