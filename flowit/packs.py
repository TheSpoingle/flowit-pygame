import json
import os
from dataclasses import dataclass

from .level import Level
from .config import packs_list_path, packs_dir_path

packs: list["Pack"] = []


class PackError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class LoadPacksError(PackError):
    pass

class GetPackError(PackError):
    pass

@dataclass
class Pack:
    name: str
    levels: list[Level]

def load_packs():
    global packs
    packs = []

    # Load and validate packs file
    if not os.path.exists(packs_list_path):
        raise LoadPacksError(message=f"Packs list file does not exist. File should be at {packs_list_path}.")
    packs_data_str = open(packs_list_path, "r").read()
    try:
        packs_data = json.loads(packs_data_str)
    except json.JSONDecodeError:
        raise LoadPacksError(message=f"Invalid JSON data in packs list file. File is at {packs_list_path}.")
    if not isinstance(packs_data, list) and all(isinstance(pack_name, str) for pack_name in packs_data):
        raise LoadPacksError(message=f"Packs list file is not a list of strings. File is at {packs_list_path}.")

    for pack_id, pack in enumerate(packs_data):
        # Load and validate each pack
        pack_path = packs_dir_path + pack + ".json"
        if not os.path.exists(pack_path):
            raise LoadPacksError(message=f"Pack {pack} does not exist. File should be at {pack_path}.")
        pack_data_str = open(pack_path, "r").read()
        try:
            pack_data = json.loads(pack_data_str)
        except:
            raise LoadPacksError(message=f"Invalid JSON data in pack file at {pack_path}.")
        if not isinstance(pack_data, list):
            raise LoadPacksError(message=f"Pack {pack} is not a list of dicts. File is at {pack_path}")
        
        # Load level from pack level JSON data
        levels: list[Level] = []
        for level_id, level_data in enumerate(pack_data):
            if not isinstance(level_data, dict):
                raise LoadPacksError(message=f"Pack {pack} is not a list of dicts. File is at {pack_path}")
            level = Level.from_dict(level_data, pack_id, level_id)
            levels.append(level)

        packs.append(Pack(name=pack, levels=levels))