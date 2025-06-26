from pathlib import Path
from typing import Any, Dict, Tuple, List
from src.state import State


def format_tile_diffs(
        tile_diffs: Dict[Tuple[int, int], Dict[str, List[str]]],
        previous: State
) -> str:
    """
    Given a dict mapping (x, y) → {'expected': [...], 'actual': [...]},
    return a string like:

    Differences at X=1,Y=2:
      - expected: [...]
      - new: [...]
    Differences at X=2,Y=0:
      ...
    """
    lines: List[str] = []

    # Sort by coordinates for deterministic order
    for (x, y) in sorted(tile_diffs.keys()):
        pre_objs = previous.get_objects_at(x, y)
        old_objs = tile_diffs[(x, y)]["expected"]
        new_objs = tile_diffs[(x, y)]["actual"]

        lines.append(f"Differences at X={x},Y={y}:")
        lines.append(f"  - previous: {pre_objs}")
        lines.append(f"  - expected: {old_objs}")
        lines.append(f"  - actual: {new_objs}")

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
