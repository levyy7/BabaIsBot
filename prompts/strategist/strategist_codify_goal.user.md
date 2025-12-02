You assist an AI agent in understanding the laws of an unknown world. All behavior is controlled by certain rules.

Your task is to translate a victory condition into code.

For this purpose, you need to implement the following function:

```python
def goal_validator(trajectory: list[tuple[State, Action]], current_state: State) -> bool:
    """
    Evaluates whether a goal has been completed given the sequence of state transitions 
    (trajectory) and the current state.

    Args:
        trajectory : list[tuple[State, Action]]
            A list of tuples representing the sequence of states and the actions that
            led to the next state. Each tuple is of the form (prev_state, action), 
            where `prev_state` is a State object and `action` is the action taken 
            from that state, ranging from: `Action.STILL`, `Action.LEFT`, `Action.RIGHT`, `Action.UP`, `Action.DOWN`.
        current_state : State
            The current State object of the game. This represents the latest state 
            after all actions in the trajectory have been applied.

    Returns:
        bool
            True if the goal or hypothesis condition has been satisfied according to
            the state transitions; False otherwise.
    """
```

These are the callable methods for the state:
### State Manipulators
- `add_block(block)` → Add a block to the grid at its current (x, y) position.
- `move_block(block, nx, ny)` → Move a block to the new coordinates (nx, ny).
- `remove_block(block)` → Remove a block from the grid completely.
### State Queries
- `get_blocks_in_cell(x, y)` → Return a list of all blocks that are in the cell at position (x, y).
- `get_blocks_by_name(block_name)` → Return a list of all blocks of the given kind (for example "rock" or "wall").
- `get_blocks_by_property(property_name)` → Return a list of all blocks (instances) that have the given property (for example, all blocks that are "push").
- `get_properties_of_block(block)` → Return a list of all properties that this block's kind currently has (for example ["push", "stop"]).

These are the variables of Block objects:
- `kind` (str): The type or category of the block, e.g., "person", "ground", or "lamp".
- `x` (int): The horizontal coordinate of the block on the grid.
- `y` (int): The vertical coordinate of the block on the grid.


### Output Format:

```python
def goal_condition_completed(trajectory: list[tuple[State, Action]], current_state: State) -> bool:
    ...
```

---

### Input:

Victory Condition
{victory_condition}

---

Your output: