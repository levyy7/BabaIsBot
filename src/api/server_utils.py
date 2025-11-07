import os
import configparser
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BABA_SOURCE_DIR = Path(os.getenv("BABA_SOURCE_DIR"))
BABA_COMMANDS_DIR = Path(os.getenv("BABA_COMMANDS_DIR"))
BABA_STATE_PATH = BABA_SOURCE_DIR / "Data" / "Worlds" / "baba" / "world_data.txt"


def read_world_state():
    config = configparser.ConfigParser()
    config.read(BABA_STATE_PATH, encoding="utf-8")

    # Get the state section and parse the units
    state_data = config["state"]["state"]
    # Each unit is separated by '€', each field by '|'
    units = [unit.split("|") for unit in state_data.split("€") if unit]

    # Convert the raw data into a list of dictionaries with proper field names
    parsed_units = []
    for unit in units:
        if len(unit) >= 21:  # Ensure we have all required fields
            parsed_unit = {
                "key": unit[0],
                "UNITNAME": unit[1],
                "UNITTYPE": unit[2],
                "XPOS": unit[3],
                "YPOS": unit[4],
                "DIR": unit[5],
                "VISUALDIR": unit[6],
                "ZLAYER": unit[7],
                "MOVED": unit[8],
                "EFFECT": unit[9],
                "COLOUR": unit[10],
                "VISUALSTYLE": unit[11],
                "VISUALLEVEL": unit[12],
                "CLEARCOLOUR": unit[13],
                "DECOR": unit[14],
                "ONLINE": unit[15],
                "COMPLETED": unit[16],
                "EFFECTCOUNT": unit[17],
                "FLOAT": unit[18],
                "A": unit[19],
                "ID": unit[20],
            }
            parsed_units.append(parsed_unit)

    # Read room size information
    room_size = None
    room_size_data = config["state"]["room_size"]
    room_size_parts = room_size_data.split("|")
    if len(room_size_parts) == 2:
        room_size = (int(room_size_parts[0]), int(room_size_parts[1]))
    # except (KeyError, ValueError):
    #     # If room size is not available, we'll compute it from units
    #     pass

    return parsed_units, room_size


def get_next_command_file():
    k = 0
    while True:
        path = os.path.join(BABA_COMMANDS_DIR, f"{k}.lua")
        if not os.path.exists(path):
            return path
        k += 1
