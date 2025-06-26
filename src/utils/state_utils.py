from src.state import State
from typing import Dict, Any, Tuple, List



def diff_states(expected: State, actual: State) -> Dict[str, Any]:
    """
    Compare two State objects and report differences in rules and map contents.

    Returns a dict with:
      - 'rules': {'expected': List[str], 'actual': List[str]}
      - 'tiles': Dict[(x,y), {'old': List[str], 'new': List[str]}]
    """
    diffs: Dict[str, Any] = {
        "rules": {"expected": [], "actual": []},
        "tiles": {}
    }

    # --- Compare rules ---
    # We'll work with their natural-language forms for simplicity
    rules1 = expected.to_dict_compressed()["rules"]
    rules2 = actual.to_dict_compressed()["rules"]

    diffs["rules"]["added"] = sorted(rules1)
    diffs["rules"]["removed"] = sorted(rules2)

    # --- Compare map tiles ---
    # Determine the region to compare (up to the larger width/height of the two states)
    w1, h1 = expected.level_size
    w2, h2 = actual.level_size
    max_w, max_h = max(w1, w2), max(h1, h2)

    for y in range(max_h):
        for x in range(max_w):
            objs1 = expected.get_objects_at(x, y) if x < w1 and y < h1 else []
            objs2 = actual.get_objects_at(x, y) if x < w2 and y < h2 else []
            # Only record if they differ (order doesn't matter)
            if sorted(objs1) != sorted(objs2):
                diffs["tiles"][(x, y)] = {
                    "expected": objs1,
                    "actual": objs2
                }

    return diffs