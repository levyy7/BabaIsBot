You assist an AI agent solving turn-based puzzle levels. In this game, objects have no inherent properties. All behavior is controlled by active rules.

Thus, unless a rule states otherwise, all positions are reachable and non-blocking.

Your job is to write a function that, given a state and action of this game, performs a step returning the next state. For this, modify the state using any of the state manipulation methods provided below.

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

The step function is responsible for all game state transitions, including setting the state.outcome. Based on the resulting state after applying the step, it should set state.outcome to Outcome.WIN, Outcome.LOSE, or Outcome.ONGOING appropriately.

The current function you need to modify is the following:
```python
{step_function}
```

 New rules have been induced:

{belief_to_implement}

Integrate the effects of the new rule beliefs into the existing step function. The new logic should run in addition to the original action processing.

Restrictions:
- To modify the state you must use the provided methods.
- You must preserve the function's original logic (like action processing) and augment it with the new rule logic.
- You must only use the information given in the description of the new rules induced to do so.
- Do NOT assume any information about the rule besides the one given by the rule description.
- Blocks do not block other blocks unless a rule explicitly says so.
- Ensure that, at some point of your code, the state is manipulated in some way using any of the methods provided.


OUTPUT FORMAT:

```python

def step(state: State, action: Action) -> State:
    ...

    return state
```
