
def step(state: State, action: Action) -> State:
    dx, dy = {
        Action.STILL: (0, 0),
        Action.UP: (-1, 0),
        Action.DOWN: (1, 0),
        Action.LEFT: (0, -1),
        Action.RIGHT: (0, 1),
    }[action]

    for row in state.grid:
        for cell in row:
            for block in cell:
                nx, ny = (block.x + dx, block.y + dy)  # new block position after action
                # ...

    state.outcome = Outcome.ONGOING
    return state 
