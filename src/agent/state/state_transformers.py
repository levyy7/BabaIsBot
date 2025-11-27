# ----------------------------
# Soft transformation
# ----------------------------
SOFT_TRANSFORM = {
    # Entities
    "BABA": "CHARACTER",
    "WALL": "BARRIER",
    "LAVA": "FIRE",
    "KEY": "TOKEN",
    "DOOR": "GATE",
    "ROCK": "STONE",

    # Properties
    "YOU": "CONTROLLABLE",
    "WIN": "GOAL",
    "PUSH": "MOVABLE",
    "STOP": "BLOCK",
    "MELT": "LIQUIFY",
    "HOT": "BURN",
    "FLAG": "BANNER",
    "DEFEAT": "LOSE",
    "OPEN": "UNLOCKER",
    "SHUT": "LOCKED",
}

# ----------------------------
# Hard transformation
# Nouns -> shapes, Properties -> colors
# ----------------------------
HARD_TRANSFORM = {
    # Entities
    "BABA": "CIRCLE",
    "ROCK": "SQUARE",
    "FLAG": "HEX",
    "KEY": "TRIANGLE",
    "DOOR": "DIAMOND",
    "WALL": "PENTAGON",

    # Properties
    "YOU": "GREEN",
    "WIN": "YELLOW",
    "PUSH": "BLUE",
    "STOP": "RED",
    "MELT": "ORANGE",
    "HOT": "RED",
    "DEFEAT": "PURPLE",
    "OPEN": "CYAN",
    "SHUT": "BROWN",
    "LAVA": "ORANGE",
}


# ----------------------------
# Automatically add TEXT_ versions
# ----------------------------
def add_text_versions(mapping):
    new_mapping = dict(mapping)  # copy
    for k, v in mapping.items():
        new_mapping[f"TEXT_{k}"] = f"TEXT_{v}"
    return new_mapping


SOFT_TRANSFORM = add_text_versions(SOFT_TRANSFORM)
HARD_TRANSFORM = add_text_versions(HARD_TRANSFORM)

# ----------------------------
# Transformation function
# ----------------------------
import copy


def symbolic_transform(state, mode="soft"):
    """
    Transform a Baba Is You state symbolically.
    mode: "soft" (preserve partial meaning) or "hard" (fully randomized)
    """
    mapping = SOFT_TRANSFORM if mode == "soft" else HARD_TRANSFORM
    new_state = copy.deepcopy(state)

    # Apply mapping to all blocks
    for x in range(len(new_state.grid)):
        for y in range(len(new_state.grid[0])):
            for block in new_state.grid[x][y]:
                block.kind = mapping.get(block.kind, block.kind)

    # Refresh rules
    new_state.refresh_rules()
    return new_state
