[INST]
You assist an AI agent solving turn-based puzzle levels.

Your job is to write a function that, given a series of states and a goal, returns if such goal has been achieved.

These are the callable methods for the State class objects:
- get_cell(x: int, y: int) -> list[Block]: Retrieve all blocks located in the cell at coordinates (x, y).
- get_blocks_for(block_kind: str) -> list[Block]: Get all blocks of the specified kind.
- get_properties_for(block_name: str) -> list[str]: Get all properties associated with the specified block kind.
- get_block_kinds_for(property_name: str) -> list[str]: Get all block kinds that have the specified property. 

These are the variables of Block class objects:
- kind (str): The type or category of the block, e.g., "person", "ground", or "lamp".
- x (int): The horizontal coordinate of the block on the grid.
- y (int): The vertical coordinate of the block on the grid.

### Constraints
- Only output the `goal_condition_completed` function.
- Only modify the content of the function, not the signature or docstring.
- Note that you only need to check the condition for the last states, as this condition has been checked for each state of the trajectory.

### Input

Goal:
{goal}

Current Knowledge:
{knowledge}

OUTPUT FORMAT:
```python
def goal_condition_completed(trajectory: list[tuple[State, Action]], current_state: State) -> bool:
    """
    Evaluates whether a hypothesis or goal has been completed given the sequence of 
    state transitions (trajectory) and the current state.

    Parameters
    ----------
    trajectory : list[tuple[State, Action]]
        A list of tuples representing the sequence of states and the actions that
        led to the next state. Each tuple is of the form (prev_state, action), 
        where `prev_state` is a State object and `action` is the action taken 
        from that state, ranging from: `Action.STILL`, `Action.LEFT`, `Action.RIGHT`, `Action.UP`, `Action.DOWN`.
    current_state : State
        The current State object of the game. This represents the latest state 
        after all actions in the trajectory have been applied.

    Returns
    -------
    bool
        True if the goal or hypothesis condition has been satisfied according to
        the state transitions; False otherwise.
    """
    ...
```
[/INST]