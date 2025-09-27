from enum import Enum, auto


class ActionType(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    STILL = auto()
    RESTART = auto()
    NEXT_LEVEL = auto()
    LOAD_LEVEL = auto()
    EXIT = auto()

    _MOVEMENT_ACTIONS = {"LEFT", "RIGHT", "UP", "DOWN", "STILL"}

    _LEVEL_MODIFIER_ACTIONS = {"RESTART", "NEXT_LEVEL", "LOAD_LEVEL"}

    def is_movement(self) -> bool:
        return self.name in self._MOVEMENT_ACTIONS

    def is_level_modifier(self) -> bool:
        return self.name in self._LEVEL_MODIFIER_ACTIONS
