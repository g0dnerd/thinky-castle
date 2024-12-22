from typing import Set


class Square:
    """Represents a node index in x/y space.
    A1 is (0, 0), E5 is (4, 4).
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{chr(ord('A') + self.x)}{1 + self.y}"

    # We need eq and hash so that stuff like
    # `if Square(1, 1) in node.walls` works.
    def __eq__(self, other):
        if not isinstance(other, Square):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class MapLayer:
    def __init__(self, size: int):
        """Creates a new square map layer of size x."""
        self.size = size
        # Initialize a two-dimensional array of empty nodes
        self.nodes = [[Node() for _ in range(size)] for _ in range(size)]

    def _validate_square(self, s: Square):
        """Ensures a square is within map bounds."""
        if not (0 <= s.x < self.size and 0 <= s.y < self.size):
            raise ValueError(f"Square {str(s)} is out of bounds.")

    def _validate_adjacent(self, a: Square, b: Square):
        """Ensures a and b are adjacent."""
        # Adjacent squares can only either be one x or one y value apart.
        if abs(a.x - b.x) + abs(a.y - b.y) != 1:
            raise ValueError(f"Squares {str(a)} and {str(b)} are not adjacent.")

    def add_wall(self, a: Square, b: Square):
        """Adds a wall between squares a and b."""
        self._validate_square(a)
        self._validate_square(b)
        self._validate_adjacent(a, b)
        self.nodes[a.y][a.x].walls.add(b)
        self.nodes[b.y][b.x].walls.add(a)

    def __str__(self) -> str:
        ret = "  "
        for i in range(self.size):
            ret += chr(ord("A") + i) + "   "
        ret += "\n"

        for y, row in enumerate(self.nodes):
            ret += f"{y+1} "
            h_walls = "  "
            for x, node in enumerate(row):
                ret += "o" if not node.contents else str(node.contents)
                ret += " | " if Square(x + 1, y) in node.walls else "   "
                h_walls += "-   " if Square(x, y + 1) in node.walls else "    "

            ret += "\n"
            ret += h_walls
            ret += "\n"
        return ret


class Node:
    """A node represents one square on a map layer.
    A node can contain things like traps or ladders.
    Nodes contain information about which other nodes they share a wall with.
    """

    def __init__(self, contents=None):
        self.contents = contents
        self.walls: Set[Square] = set()
