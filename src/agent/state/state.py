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
        self.kind_to_properties: dict[str, list[str]] = (
            self._compute_kind_to_properties()
        )
        self.property_to_kinds: dict[str, list[str]] = self._compute_property_to_kinds()
        self.outcome = Outcome.ONGOING

        # grid indexed as [y][x]: height rows, width columns
        # grid = [[[] for _ in range(height)] for _ in range(width)]
        #
        # for block_name, position_list in dto.blocks.items():
        #     for position in position_list:
        #         block = Block(block_name, position["y"], position["x"])
        #         # use y first, then x
        #         grid[block.x][block.y].append(block)
        #
        # # rules = {}
        # # for block_name, rule in dto.rules.items():
        # #     rules[block_name] = list(map(lambda x: x.value(), rule))

    @classmethod
    def from_grid_string(cls, grid_str: str) -> "State":
        lines = grid_str.strip().splitlines()

        # Extract header row with Y coordinate labels
        header_parts = [p.strip() for p in lines[0].split("|")]
        y_labels = header_parts[1:]  # skip the x/y label
        height = len(y_labels)

        # Remove the separator line
        data_lines = lines[2:]

        # Extract X labels from first column of each row
        x_labels = [p.strip() for p in (line.split("|")[0] for line in data_lines)]
        width = len(x_labels)

        # Create empty grid[x][y]
        grid: list[list[list[Block]]] = [
            [[] for _ in range(height)] for _ in range(width)
        ]

        for x_index, line in enumerate(data_lines):
            parts = [p.strip() for p in line.split("|")]
            # parts[0] is X label, skip it
            cell_values = parts[1:]
            for y_index, cell in enumerate(cell_values):
                if cell:
                    for name in cell.split(","):
                        grid[x_index][y_index].append(Block(name, x_index, y_index))

        return cls(grid)

    def __eq__(self, other):
        self.sort_cells_lexicographically()
        if isinstance(other, State):
            other.sort_cells_lexicographically()

        return isinstance(other, State) and self.grid == other.grid

    def __hash__(self):
        # Convert the 3D list into a tuple of tuples so it's hashable
        self.sort_cells_lexicographically()
        return hash(
            tuple(
                tuple(tuple(block for block in cell) for cell in row)
                for row in self.grid
            )
        )

    def __repr__(self):
        lines = []
        for x in range(len(self.grid)):  # outer loop is X
            col_str = []
            for y in range(len(self.grid[0])):  # inner loop is Y
                cell = self.grid[x][y]
                col_str.append(",".join(b.kind for b in cell) or ".")
            lines.append(" ".join(col_str))
        return "\n".join(lines)

    def __str__(self) -> str:
        width, height = len(self.grid[0]), len(self.grid)

        # Build a 2D grid initialized with empty strings
        grid = [["" for _ in range(width)] for _ in range(height)]

        # Fill in grid with block names (converted to lowercase)
        for x in range(height):
            for y in range(width):
                existing = self.grid[x][y]
                grid[x][y] = ", ".join(list(map(lambda block: block.kind, existing)))

        # Compute max width for each column
        col_widths = []
        for x in range(width):
            max_len = max(len(grid[y][x]) for y in range(height))
            max_len = max(max_len, len(str(x + 1)))  # also account for header number
            col_widths.append(max(max_len, 4))  # minimum width for visibility

        # Generate header
        header = ["y/x".rjust(4)] + [
            str(i + 1).center(col_widths[i]) for i in range(width)
        ]
        separator = "-----+" + "+".join("-" * (w + 1) for w in col_widths)

        # Generate rows
        rows = [" |".join(header), separator]
        for y in range(height):
            row = [str(y + 1).rjust(4)] + [
                grid[y][x].center(col_widths[x]) if grid[y][x] else " " * col_widths[x]
                for x in range(width)
            ]
            rows.append(" |".join(row))

        return "\n".join(rows)

    def sort_cells_lexicographically(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                self.grid[x][y].sort(key=lambda block: block.kind)

    def print_rules(self) -> str:
        rules = {
            f"{'text' if kind.startswith('text_') else kind} IS {'text' if prop.startswith('text_') else prop}"
            for kind, property_list in self.kind_to_properties.items()
            for prop in property_list
        }

        return "\n".join(rules)

    def add_block(self, block):
        """Place a block on the grid."""
        self.grid[block.x][block.y].append(block)
        self.kind_to_blocks = self._compute_kind_to_blocks()

    def move(self, block: Block, nx: int, ny: int):
        """Move a block and update the grid."""
        if nx >= len(self.grid) or nx < 0 or ny >= len(self.grid[0]) or ny < 0:
            print(
                f"WARNING: Trying to move outside map: from ({block.x}, {block.y}) to ({nx}, {ny})"
            )
            print(block)
            return

        # Remove from old position
        self.grid[block.x][block.y].remove(block)

        # Update coordinates
        block.x = nx
        block.y = ny

        # Add to new position
        self.grid[block.x][block.y].append(block)
        self.kind_to_blocks = self._compute_kind_to_blocks()

    def delete(self, block):
        """Remove a block from the grid entirely."""
        self.grid[block.x][block.y].remove(block)
        self.kind_to_blocks = self._compute_kind_to_blocks()

    def get_cell(self, x, y) -> list[Block]:
        """Get all blocks in a cell."""
        return self.grid[x][y]

    def get_blocks_for(self, block_kind: str) -> list[Block]:
        return self.kind_to_blocks.get(block_kind, [])

    def get_properties_for(self, block_name: str) -> list[str]:
        return self.kind_to_properties.get(block_name, [])

    def get_block_kinds_for(self, property_name: str) -> list[str]:
        # print(self.property_to_kinds)
        return self.property_to_kinds.get(property_name, [])

    def refresh_rules(self):
        self.kind_to_properties = self._compute_kind_to_properties()
        self.property_to_kinds = self._compute_property_to_kinds()

    def _compute_kind_to_blocks(self) -> dict[str, list[Block]]:
        """
        Needs self.grid to be defined
        :return:
        """
        kind_to_blocks: Dict[str, List[Block]] = {}

        for row in self.grid:
            for block_list in row:
                for block in block_list:
                    if block.kind not in kind_to_blocks.keys():
                        kind_to_blocks[block.kind] = []

                    kind_to_blocks[block.kind].append(block)

        return kind_to_blocks

    def _compute_kind_to_properties(self) -> dict[str, list[str]]:
        """
        Parse rules from the grid and populate self.kind_to_properties
        as { noun_kind: [property1, property2, ...] }.
        Assumes rules are in the form NOUN IS PROPERTY,
        read left-to-right or top-to-bottom.
        """
        kind_to_properties: dict[str, list[str]] = {}

        rows = len(self.grid)
        cols = len(self.grid[0]) if rows > 0 else 0

        # Check horizontally
        for x in range(rows):
            for y in range(cols - 2):
                kinds1 = self._get_kinds(x, y)
                kinds2 = self._get_kinds(x, y + 1)
                kinds3 = self._get_kinds(x, y + 2)

                if "text_is" in kinds2:
                    for noun in kinds1:
                        for prop in kinds3:
                            if noun in noun_types and prop in (
                                noun_types + property_types
                            ):
                                self._add_rule(
                                    kind_to_properties,
                                    noun_references_to(noun),
                                    prop.removeprefix("text_"),
                                )

        # Check vertically
        for x in range(rows - 2):
            for y in range(cols):
                kinds1 = self._get_kinds(x, y)
                kinds2 = self._get_kinds(x + 1, y)
                kinds3 = self._get_kinds(x + 2, y)

                if "IS" in kinds2:
                    for noun in kinds1:
                        for prop in kinds3:
                            if noun in noun_types and prop in (
                                noun_types + property_types
                            ):
                                self._add_rule(
                                    kind_to_properties,
                                    noun_references_to(noun),
                                    prop.removeprefix("text_"),
                                )

        for x in range(rows):
            for y in range(cols):
                kinds = self._get_kinds(x, y)

                for kind in kinds:
                    if kind.startswith("text_"):
                        self._add_rule(kind_to_properties, kind, "push")

        return kind_to_properties

    def _compute_property_to_kinds(self) -> dict[str, list[str]]:
        property_to_kinds: dict[str, list[str]] = {}

        for kind, properties in self.kind_to_properties.items():
            for rule_property in properties:
                if rule_property not in property_to_kinds.keys():
                    property_to_kinds[rule_property] = []

                property_to_kinds[rule_property].append(kind)

        return property_to_kinds

    def _add_rule(self, kind_to_properties: dict[str, list[str]], noun: str, prop: str):
        if noun not in kind_to_properties:
            kind_to_properties[noun] = []
        if prop not in kind_to_properties[noun]:
            kind_to_properties[noun].append(prop)

    # Helper to get block kinds at a grid position
    def _get_kinds(self, x: int, y: int) -> list[str]:
        return [b.kind for b in self.grid[x][y]]
