from typing import Any, Dict, List, Tuple
from dataclasses import dataclass, asdict
import json

from src.state.block_type import BlockType


@dataclass
class State:
    rules: Dict[str, List[Dict[str, str]]]
    level_id: int
    level_name: str
    level_size: Tuple[int, int]
    level_completed: bool
    blocks: Dict[str, List[Dict[str, int]]]

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "State":
        return cls(
            rules=raw.get("rules", {}),
            level_id=raw.get("levelId", -1),
            level_name=raw.get("levelName", ""),
            level_size=tuple(raw.get("levelSize", (0, 0))),
            level_completed=raw.get("levelCompleted", False),
            blocks=raw.get("blocks", {}),
        )

    def __str__(self) -> str:
        width, height = self.level_size
        rows = []
        used_blocks = set()

        for y in range(height):
            row = []
            for x in range(width):
                blocks = self.get_objects_at(x, y)
                if not blocks:
                    # No blocks at this position
                    block_id = BlockType["EMPTY"]
                else:
                    # Take the first block type present (or decide your priority)
                    block_name = blocks[0]
                    block_id = BlockType[block_name]
                row.append(block_id)
                used_blocks.add(block_id)
            rows.append(' '.join(f"{num:>3}" for num in row))

        legend = ["Legend:"]
        for block_id in sorted(used_blocks):
            legend.append(f"{block_id} = {BlockType(block_id).name}")

        return "\n".join(rows) + "\n\n" + "\n".join(legend)

    def get_objects_at(self, x: int, y: int) -> List[str]:
        found = []
        for block_type, positions in self.blocks.items():
            for pos in positions:
                if pos.get("x") == x and pos.get("y") == y:
                    found.append(block_type)
        return found

    def get_rule_for(self, subject: str) -> List[Dict[str, str]]:
        return self.rules.get(subject, [])

    def is_win(self) -> bool:
        return self.level_completed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rules": self.rules,
            "levelId": self.level_id,
            "levelName": self.level_name,
            "levelSize": list(self.level_size),
            "levelCompleted": self.level_completed,
            "blocks": self.blocks,
        }

    def to_dict_compressed(self) -> Dict[str, Any]:
        nl_rules: List[str] = [
            f"{rule['subject']} {rule['verb']} {rule['object']}"
            for rules in self.rules.values()
            for rule in rules
        ]

        width, height = self.level_size
        game_map: List[List[List[str]]] = [
            [self.get_objects_at(x, y) for x in range(width)]
            for y in range(height)
        ]

        return {
            "rules": nl_rules,
            "map": game_map,
        }


if __name__ == "__main__":
    state = State.from_dict({
        "levelSize": [33, 18],
        "blocks": {
    "BABA": [
      {
        "x": 16,
        "y": 9
      }
    ],
    "MELT": [
      {
        "x": 10,
        "y": 12
      }
    ],
    "TEXT_BABA": [
      {
        "x": 7,
        "y": 3
      },
      {
        "x": 8,
        "y": 12
      }
    ],
    "FLAG": [
      {
        "x": 26,
        "y": 12
      }
    ],
    "ROCK": [
      {
        "x": 14,
        "y": 5
      }
    ],
    "HOT": [
      {
        "x": 10,
        "y": 14
      }
    ],
    "TEXT_FLAG": [
      {
        "x": 25,
        "y": 14
      }
    ],
    "PUSH": [
      {
        "x": 7,
        "y": 9
      }
    ],
    "WALL": [
      {
        "x": 6,
        "y": 0
      },
      {
        "x": 6,
        "y": 1
      },
      {
        "x": 6,
        "y": 2
      },
      {
        "x": 6,
        "y": 3
      },
      {
        "x": 6,
        "y": 4
      },
      {
        "x": 6,
        "y": 5
      },
      {
        "x": 6,
        "y": 6
      },
      {
        "x": 6,
        "y": 7
      },
      {
        "x": 7,
        "y": 4
      },
      {
        "x": 7,
        "y": 6
      },
      {
        "x": 7,
        "y": 12
      },
      {
        "x": 7,
        "y": 13
      },
      {
        "x": 7,
        "y": 14
      },
      {
        "x": 7,
        "y": 15
      },
      {
        "x": 8,
        "y": 6
      },
      {
        "x": 8,
        "y": 7
      },
      {
        "x": 8,
        "y": 13
      },
      {
        "x": 8,
        "y": 15
      },
      {
        "x": 9,
        "y": 6
      },
      {
        "x": 9,
        "y": 13
      },
      {
        "x": 9,
        "y": 15
      },
      {
        "x": 10,
        "y": 6
      },
      {
        "x": 10,
        "y": 13
      },
      {
        "x": 10,
        "y": 15
      },
      {
        "x": 11,
        "y": 4
      },
      {
        "x": 11,
        "y": 6
      },
      {
        "x": 11,
        "y": 12
      },
      {
        "x": 11,
        "y": 13
      },
      {
        "x": 11,
        "y": 14
      },
      {
        "x": 11,
        "y": 15
      },
      {
        "x": 12,
        "y": 0
      },
      {
        "x": 12,
        "y": 2
      },
      {
        "x": 12,
        "y": 3
      },
      {
        "x": 12,
        "y": 4
      },
      {
        "x": 12,
        "y": 6
      },
      {
        "x": 13,
        "y": 3
      },
      {
        "x": 14,
        "y": 3
      },
      {
        "x": 15,
        "y": 3
      },
      {
        "x": 16,
        "y": 0
      },
      {
        "x": 16,
        "y": 1
      },
      {
        "x": 16,
        "y": 2
      },
      {
        "x": 16,
        "y": 3
      }
    ],
    "TEXT_LAVA": [
      {
        "x": 8,
        "y": 14
      },
      {
        "x": 12,
        "y": 10
      }
    ],
    "IS": [
      {
        "x": 1,
        "y": 0
      },
      {
        "x": 7,
        "y": 8
      },
      {
        "x": 8,
        "y": 3
      },
      {
        "x": 9,
        "y": 12
      },
      {
        "x": 9,
        "y": 14
      },
      {
        "x": 26,
        "y": 14
      }
    ],
    "LAVA": [
      {
        "x": 0,
        "y": 1
      },
      {
        "x": 0,
        "y": 2
      },
      {
        "x": 0,
        "y": 3
      },
      {
        "x": 1,
        "y": 1
      },
      {
        "x": 1,
        "y": 2
      },
      {
        "x": 2,
        "y": 1
      },
      {
        "x": 3,
        "y": 0
      },
      {
        "x": 3,
        "y": 1
      },
      {
        "x": 4,
        "y": 0
      },
      {
        "x": 11,
        "y": 17
      },
      {
        "x": 12,
        "y": 16
      },
      {
        "x": 12,
        "y": 17
      },
      {
        "x": 13,
        "y": 15
      },
      {
        "x": 13,
        "y": 16
      },
      {
        "x": 13,
        "y": 17
      },
      {
        "x": 14,
        "y": 13
      },
      {
        "x": 14,
        "y": 14
      },
      {
        "x": 14,
        "y": 15
      },
      {
        "x": 14,
        "y": 16
      },
      {
        "x": 14,
        "y": 17
      },
      {
        "x": 15,
        "y": 11
      },
      {
        "x": 15,
        "y": 12
      },
      {
        "x": 15,
        "y": 13
      },
      {
        "x": 15,
        "y": 14
      },
      {
        "x": 15,
        "y": 15
      },
      {
        "x": 15,
        "y": 16
      },
      {
        "x": 15,
        "y": 17
      },
      {
        "x": 16,
        "y": 9
      },
      {
        "x": 16,
        "y": 10
      },
      {
        "x": 16,
        "y": 11
      },
      {
        "x": 16,
        "y": 12
      },
      {
        "x": 16,
        "y": 13
      },
      {
        "x": 16,
        "y": 14
      },
      {
        "x": 16,
        "y": 15
      },
      {
        "x": 16,
        "y": 16
      },
      {
        "x": 16,
        "y": 17
      },
      {
        "x": 17,
        "y": 6
      },
      {
        "x": 17,
        "y": 7
      },
      {
        "x": 17,
        "y": 8
      },
      {
        "x": 17,
        "y": 9
      },
      {
        "x": 17,
        "y": 10
      },
      {
        "x": 17,
        "y": 11
      },
      {
        "x": 17,
        "y": 12
      },
      {
        "x": 17,
        "y": 13
      },
      {
        "x": 17,
        "y": 14
      },
      {
        "x": 17,
        "y": 15
      },
      {
        "x": 17,
        "y": 16
      },
      {
        "x": 17,
        "y": 17
      },
      {
        "x": 18,
        "y": 3
      },
      {
        "x": 18,
        "y": 4
      },
      {
        "x": 18,
        "y": 5
      },
      {
        "x": 18,
        "y": 6
      },
      {
        "x": 18,
        "y": 7
      },
      {
        "x": 18,
        "y": 8
      },
      {
        "x": 18,
        "y": 9
      },
      {
        "x": 18,
        "y": 10
      },
      {
        "x": 18,
        "y": 11
      },
      {
        "x": 18,
        "y": 12
      },
      {
        "x": 18,
        "y": 13
      },
      {
        "x": 18,
        "y": 14
      },
      {
        "x": 18,
        "y": 15
      },
      {
        "x": 19,
        "y": 1
      },
      {
        "x": 19,
        "y": 2
      },
      {
        "x": 19,
        "y": 3
      },
      {
        "x": 19,
        "y": 4
      },
      {
        "x": 19,
        "y": 5
      },
      {
        "x": 19,
        "y": 6
      },
      {
        "x": 19,
        "y": 7
      },
      {
        "x": 19,
        "y": 8
      },
      {
        "x": 19,
        "y": 9
      },
      {
        "x": 19,
        "y": 10
      },
      {
        "x": 19,
        "y": 11
      },
      {
        "x": 19,
        "y": 12
      },
      {
        "x": 19,
        "y": 13
      },
      {
        "x": 20,
        "y": 0
      },
      {
        "x": 20,
        "y": 1
      },
      {
        "x": 20,
        "y": 2
      },
      {
        "x": 20,
        "y": 3
      },
      {
        "x": 20,
        "y": 4
      },
      {
        "x": 20,
        "y": 5
      },
      {
        "x": 20,
        "y": 6
      },
      {
        "x": 20,
        "y": 7
      },
      {
        "x": 20,
        "y": 8
      },
      {
        "x": 20,
        "y": 9
      },
      {
        "x": 20,
        "y": 10
      },
      {
        "x": 20,
        "y": 11
      },
      {
        "x": 20,
        "y": 12
      },
      {
        "x": 21,
        "y": 0
      },
      {
        "x": 21,
        "y": 1
      },
      {
        "x": 21,
        "y": 2
      },
      {
        "x": 21,
        "y": 3
      },
      {
        "x": 21,
        "y": 4
      },
      {
        "x": 21,
        "y": 5
      },
      {
        "x": 21,
        "y": 6
      },
      {
        "x": 21,
        "y": 7
      },
      {
        "x": 21,
        "y": 8
      },
      {
        "x": 21,
        "y": 9
      },
      {
        "x": 21,
        "y": 10
      },
      {
        "x": 22,
        "y": 0
      },
      {
        "x": 22,
        "y": 1
      },
      {
        "x": 22,
        "y": 2
      },
      {
        "x": 22,
        "y": 3
      },
      {
        "x": 22,
        "y": 4
      },
      {
        "x": 22,
        "y": 5
      },
      {
        "x": 22,
        "y": 6
      },
      {
        "x": 22,
        "y": 7
      },
      {
        "x": 22,
        "y": 8
      },
      {
        "x": 22,
        "y": 9
      },
      {
        "x": 23,
        "y": 0
      },
      {
        "x": 23,
        "y": 1
      },
      {
        "x": 23,
        "y": 2
      },
      {
        "x": 23,
        "y": 3
      },
      {
        "x": 23,
        "y": 4
      },
      {
        "x": 23,
        "y": 5
      },
      {
        "x": 23,
        "y": 6
      },
      {
        "x": 24,
        "y": 0
      },
      {
        "x": 24,
        "y": 1
      },
      {
        "x": 24,
        "y": 2
      },
      {
        "x": 24,
        "y": 3
      },
      {
        "x": 25,
        "y": 0
      },
      {
        "x": 25,
        "y": 1
      },
      {
        "x": 26,
        "y": 0
      },
      {
        "x": 30,
        "y": 17
      },
      {
        "x": 31,
        "y": 16
      },
      {
        "x": 31,
        "y": 17
      },
      {
        "x": 32,
        "y": 15
      },
      {
        "x": 32,
        "y": 16
      },
      {
        "x": 32,
        "y": 17
      }
    ],
    "STOP": [
      {
        "x": 2,
        "y": 0
      }
    ],
    "TEXT_ROCK": [
      {
        "x": 7,
        "y": 7
      }
    ],
    "TEXT_WALL": [
      {
        "x": 0,
        "y": 0
      }
    ],
    "WIN": [
      {
        "x": 27,
        "y": 14
      }
    ],
    "YOU": [
      {
        "x": 9,
        "y": 3
      }
    ]
  }
    })
    print(state)