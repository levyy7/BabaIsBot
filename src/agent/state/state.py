from src.agent.state.block import Block
from src.agent.state.outcomes import Outcome
from src.agent.state.block_type import (
    noun_references_to,
    block_types,
    noun_types,
    verb_types,
    property_types,
)


class State:
    def __init__(self, grid):
        self.grid: list[list[list[Block]]] = grid
        self.kind_to_blocks: dict[str, list[Block]] = self._compute_kind_to_blocks()
        self.kind_to_properties: dict[str, list[str]] = self._compute_kind_to_properties()
        self.property_to_kinds: dict[str, list[str]] = self._compute_property_to_kinds()
        self.outcome = Outcome.ONGOING

    # -------------------------------
    # Construction and Representation
    # -------------------------------

    @classmethod
    def from_grid_string(cls, grid_str: str) -> "State":
        """Create a State from a formatted grid string."""
        lines = grid_str.strip().splitlines()

        header_parts = [p.strip() for p in lines[0].split("|")]
        y_labels = header_parts[1:]
        height = len(y_labels)

        data_lines = lines[2:]
        x_labels = [p.strip() for p in (line.split("|")[0] for line in data_lines)]
        width = len(x_labels)

        grid: list[list[list[Block]]] = [
            [[] for _ in range(height)] for _ in range(width)
        ]

        for x_index, line in enumerate(data_lines):
            parts = [p.strip() for p in line.split("|")]
            cell_values = parts[1:]
            for y_index, cell in enumerate(cell_values):
                if cell:
                    for name in cell.split(","):
                        grid[x_index][y_index].append(Block(name.upper(), x_index, y_index))

        return cls(grid)

    def __eq__(self, other):
        self.sort_cells_lexicographically()
        if isinstance(other, State):
            other.sort_cells_lexicographically()
        return isinstance(other, State) and self.grid == other.grid

    def __hash__(self):
        self.sort_cells_lexicographically()
        return hash(
            tuple(
                tuple(tuple(block for block in cell) for cell in row)
                for row in self.grid
            )
        )

    def __repr__(self):
        lines = []
        for x in range(len(self.grid)):
            col_str = []
            for y in range(len(self.grid[0])):
                cell = self.grid[x][y]
                col_str.append(",".join(b.kind for b in cell) or ".")
            lines.append(" ".join(col_str))
        return "\n".join(lines)

    def __str__(self) -> str:
        width, height = len(self.grid[0]), len(self.grid)
        grid = [["" for _ in range(width)] for _ in range(height)]

        for x in range(height):
            for y in range(width):
                existing = self.grid[x][y]
                grid[x][y] = ", ".join(block.kind for block in existing)

        col_widths = []
        for x in range(width):
            max_len = max(len(grid[y][x]) for y in range(height))
            max_len = max(max_len, len(str(x + 1)))
            col_widths.append(max(max_len, 4))

        header = ["y/x".rjust(4)] + [str(i + 1).center(col_widths[i]) for i in range(width)]
        separator = "-----+" + "+".join("-" * (w + 1) for w in col_widths)

        rows = [" |".join(header), separator]
        for y in range(height):
            row = [str(y + 1).rjust(4)] + [
                grid[y][x].center(col_widths[x]) if grid[y][x] else " " * col_widths[x]
                for x in range(width)
            ]
            rows.append(" |".join(row))
        return "\n".join(rows)

    # -------------------------------
    # Grid manipulation
    # -------------------------------

    def add_block(self, block):
        """Add a block to the grid."""
        self.grid[block.x][block.y].append(block)
        self.kind_to_blocks = self._compute_kind_to_blocks()

    def move_block(self, block: Block, nx: int, ny: int):
        """Move a block to new coordinates."""
        if nx >= len(self.grid) or nx < 0 or ny >= len(self.grid[0]) or ny < 0:
            print(f"WARNING: Trying to move outside map: ({block.x}, {block.y}) → ({nx}, {ny})")
            print(block)
            return

        self.grid[block.x][block.y].remove(block)
        block.x, block.y = nx, ny
        self.grid[nx][ny].append(block)
        self.kind_to_blocks = self._compute_kind_to_blocks()

    def remove_block(self, block):
        """Remove a block completely from the grid."""
        self.grid[block.x][block.y].remove(block)
        self.kind_to_blocks = self._compute_kind_to_blocks()

    # -------------------------------
    # Queries
    # -------------------------------

    def get_blocks_in_cell(self, x, y) -> list[Block]:
        """Return all blocks in a specific grid cell."""
        return self.grid[x][y]

    def get_blocks_by_name(self, block_name: str) -> list[Block]:
        """Return all blocks of the specified kind."""
        return self.kind_to_blocks.get(block_name, [])

    def get_blocks_by_property(self, property_name: str) -> list[Block]:
        """Return all blocks (instances) that have the given property."""
        kinds = self.property_to_kinds.get(property_name, [])
        return [block for kind in kinds for block in self.kind_to_blocks.get(kind, [])]

    def get_properties_of_block(self, block: Block) -> list[str]:
        return self.kind_to_properties.get(block.kind, [])

    # -------------------------------
    # Rule management
    # -------------------------------

    def refresh_rules(self):
        """Recompute all rules and relationships."""
        self.kind_to_properties = self._compute_kind_to_properties()
        self.property_to_kinds = self._compute_property_to_kinds()

    def print_rules(self) -> str:
        rules = {
            f"{'text' if k.startswith('text_') else k} IS {'text' if p.startswith('text_') else p}"
            for k, plist in self.kind_to_properties.items()
            for p in plist
        }
        return "\n".join(sorted(rules))

    # -------------------------------
    # Internal helpers
    # -------------------------------

    def sort_cells_lexicographically(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                self.grid[x][y].sort(key=lambda b: b.kind)

    def _compute_kind_to_blocks(self) -> dict[str, list[Block]]:
        kind_to_blocks: dict[str, list[Block]] = {}
        for row in self.grid:
            for cell in row:
                for block in cell:
                    kind_to_blocks.setdefault(block.kind, []).append(block)
        return kind_to_blocks

    def _compute_kind_to_properties(self) -> dict[str, list[str]]:
        kind_to_properties: dict[str, list[str]] = {}
        rows = len(self.grid)
        cols = len(self.grid[0]) if rows > 0 else 0

        # Horizontal rules
        for x in range(rows):
            for y in range(cols - 2):
                kinds1 = self._get_kinds(x, y)
                kinds2 = self._get_kinds(x, y + 1)
                kinds3 = self._get_kinds(x, y + 2)

                if "TEXT_IS" in kinds2:
                    for noun in kinds1:
                        for prop in kinds3:
                            if noun.lower() in noun_types and prop.lower() in (noun_types + property_types):
                                self._add_rule(kind_to_properties, noun_references_to(noun), prop.removeprefix("TEXT_"))

        # Vertical rules
        for x in range(rows - 2):
            for y in range(cols):
                kinds1 = self._get_kinds(x, y)
                kinds2 = self._get_kinds(x + 1, y)
                kinds3 = self._get_kinds(x + 2, y)

                if "TEXT_IS" in kinds2:
                    for noun in kinds1:
                        for prop in kinds3:
                            if noun.lower() in noun_types and prop.lower() in (noun_types + property_types):
                                self._add_rule(kind_to_properties, noun_references_to(noun), prop.removeprefix("TEXT_"))

        # "text_*" blocks are pushable
        for x in range(rows):
            for y in range(cols):
                kinds = self._get_kinds(x, y)
                for kind in kinds:
                    if kind.startswith("TEXT_"):
                        self._add_rule(kind_to_properties, kind, "PUSH")

        return kind_to_properties

    def _compute_property_to_kinds(self) -> dict[str, list[str]]:
        property_to_kinds: dict[str, list[str]] = {}
        for kind, props in self.kind_to_properties.items():
            for prop in props:
                property_to_kinds.setdefault(prop, []).append(kind)
        return property_to_kinds

    def _add_rule(self, kind_to_properties: dict[str, list[str]], noun: str, prop: str):
        kind_to_properties.setdefault(noun, [])
        if prop not in kind_to_properties[noun]:
            kind_to_properties[noun].append(prop)

    def _get_kinds(self, x: int, y: int) -> list[str]:
        return [b.kind for b in self.grid[x][y]]
