from pathlib import Path
from typing import Any, Dict, Tuple, List
from src.agent.state import State


def format_tile_diffs(
    previous: State,
    simulated: State,
    real: State,
) -> str:
    """
    Given a dict mapping (x, y) → {'expected': [...], 'real': [...]},
    return a string like:

    Differences at X=1,Y=2:
      - expected: [...]
      - new: [...]
    Differences at X=2,Y=0:
      ...
    """
    lines: List[str] = []

    for x in range(len(previous.grid)):
        for y in range(len(previous.grid[0])):
            if simulated.get_cell(x, y) != real.get_cell(x, y):
                previous_kinds = list(
                    map(lambda block: block.kind, previous.get_cell(x, y))
                )
                simulated_kinds = list(
                    map(lambda block: block.kind, simulated.get_cell(x, y))
                )
                real_kinds = list(map(lambda block: block.kind, real.get_cell(x, y)))

                lines.append(f"Differences at X={x},Y={y}:")
                lines.append(f"  - pre-action              : {previous_kinds}")
                lines.append(f"  - post-action (real)      : {real_kinds}")
                lines.append(f"  - post-action (simulated) : {simulated_kinds}")

    return "\n".join(lines)


def load_and_format_prompt(module: str, name: str, **kwargs: Any) -> Dict[str, str]:
    """
    Load .system.md and .user.md for the given module/name pair,
    format them with kwargs, and return a dict of roles→content.
    """
    base = Path(__file__).parent.parent / "prompts" / module / name
    system_path = base.with_suffix(".system.md")
    user_path = base.with_suffix(".user.md")

    system = system_path.read_text().format(**kwargs) if system_path.exists() else ""
    user = user_path.read_text().format(**kwargs)

    return {"system": system, "user": user}
