class Block:
    def __init__(self, kind: str, x: int, y: int):
        self.kind = kind  # e.g., "BABA", "WALL", "FLAG"
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (
            isinstance(other, Block)
            and self.kind == other.kind
            and self.x == other.x
            and self.y == other.y
        )

    def __hash__(self):
        return hash((self.kind, self.x, self.y))

    def __repr__(self):
        return f"Block({self.kind}, {self.x}, {self.y})"
