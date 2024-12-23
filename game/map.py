from enum import Enum
from typing import Dict, Optional


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


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


class Node:
    """A node represents one square on a map layer.
    A node can contain things like traps or ladders.
    Nodes contain information about which other nodes they share a wall with.
    """

    def __init__(self, pos: Square):
        self.pos = pos
        self.contents = None
        self.connected_nodes: Dict[Direction, "Node"] = {}

    def connect(self, dir: Direction, target: "Node"):
        self.connected_nodes[dir] = target

    def is_accessible(self, dir):
        return dir in self.connected_nodes


class MapLayer:
    def __init__(self, size: int):
        """Creates a new square map layer of size x."""
        self.size = size
        # Initialize a two-dimensional array of empty nodes
        self.nodes = [[Node(Square(x, y)) for y in range(size)] for x in range(size)]
        self.connect_nodes()

    def connect_nodes(self):
        """Automatically connects adjacent nodes."""
        for x in range(self.size):
            for y in range(self.size):
                node = self.get_node(Square(x, y))
                assert node
                for direction in Direction:
                    dx = direction.value[0]
                    dy = direction.value[1]
                    neighbor = self.get_node(Square(x + dx, y + dy))
                    if neighbor:
                        node.connect(direction, neighbor)

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
        """Adds a wall between two nodes."""
        node1 = self.get_node(a)
        node2 = self.get_node(b)
        if node1 and node2:
            # Remove connectivity in both directions
            for direction, node in node1.connected_nodes.items():
                if node == node2:
                    del node1.connected_nodes[direction]
                    break
            for direction, node in node2.connected_nodes.items():
                if node == node1:
                    del node2.connected_nodes[direction]
                    break

    def get_node(self, s: Square) -> Optional[Node]:
        if 0 <= s.x < self.size and 0 <= s.y < self.size:
            return self.nodes[s.x][s.y]
        return None

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
                if x < self.size - 1:
                    ret += "   " if node.is_accessible(Direction.RIGHT) else " | "
                if y < self.size - 1:
                    h_walls += "    " if node.is_accessible(Direction.DOWN) else "-   "

            ret += "\n"
            ret += h_walls
            ret += "\n"
        return ret
