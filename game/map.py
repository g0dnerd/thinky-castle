from enum import Enum
from typing import Dict, Optional

from game.props import Prop


class Direction(Enum):
    """Movement directions in the lateral plane"""

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

    @classmethod
    def from_name(cls, n: str):
        """Parses a square descriptor like 'A4' into x and y coords."""
        assert len(n) == 2, "Invalid square name"

        name = n.upper()
        file_idx = ord(name[0]) - ord("A")  # A = 0, B = 1, C = 2, etc.
        rank_idx = int(name[1]) - 1

        assert 0 <= rank_idx <= 10, f"Rank {n[0]} is out of bounds."
        assert 0 <= file_idx <= 10, f"File {n[1]} is out of bounds."

        return cls(rank_idx, file_idx)

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
    Nodes contain information about which other nodes they are connected to.
    """

    def __init__(self, pos: Square):
        self.pos = pos
        self.prop = None
        self.connected_nodes: Dict[Direction, "Node"] = {}

    def connect(self, dir: Direction, target: "Node"):
        """Adds the target node as the connected node in the specified direction."""
        self.connected_nodes[dir] = target

    def is_accessible(self, dir):
        """If there is a connected node in the specified direction,
        returns it and false otherwise.
        """
        try:
            node = self.connected_nodes[dir]
            return node
        except KeyError:
            return False

    def add_prop(self, prop: Prop):
        if not self.prop:
            self.prop = prop


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
                assert node, f"Expected node in map layer at {x}, {y}, but got None."

                for dir in Direction:
                    dx = dir.value[0]
                    dy = dir.value[1]

                    # Try to get the node in the given direction
                    neighbor = self.get_node(Square(x + dx, y + dy))
                    if neighbor:
                        # If one exists, connect it to the current node.
                        node.connect(dir, neighbor)

    def add_wall(self, a: Square, b: Square):
        """Adds a wall between two nodes."""
        node1 = self.get_node(a)
        node2 = self.get_node(b)
        if node1 and node2:
            # Remove connectivity in both directions
            for dir, node in node1.connected_nodes.items():
                if node == node2:
                    del node1.connected_nodes[dir]
                    break
            for dir, node in node2.connected_nodes.items():
                if node == node1:
                    del node2.connected_nodes[dir]
                    break

    def get_node(self, s: Square) -> Optional[Node]:
        """Returns the node at the specified square in this layer if it exists
        and None otherwise.
        """
        if 0 <= s.x < self.size and 0 <= s.y < self.size:
            return self.nodes[s.x][s.y]

        return None

    def add_prop(self, s: Square, p: Prop):
        node = self.get_node(s)
        assert node, f"Could not find node on square {s} to add prop to"

        node.add_prop(p)

    def __str__(self) -> str:
        """The most cursed string representation known to man"""
        repr = "  "

        # Add file indices
        for i in range(self.size):
            repr += chr(ord("A") + i) + "   "
        repr += "\n"

        for y, row in enumerate(self.nodes):
            # Add rank indices
            repr += f"{y+1} "
            horizontal_walls = "  "

            for x, node in enumerate(row):
                repr += "o" if not node.prop else str(node.prop)
                if x < self.size - 1:
                    repr += "   " if node.is_accessible(Direction.RIGHT) else " | "
                if y < self.size - 1:
                    horizontal_walls += (
                        "    " if node.is_accessible(Direction.DOWN) else "-   "
                    )
            repr += f"\n{horizontal_walls}\n"

        return repr


class Map:
    """Holds any number of vertically arranged map layers."""

    def __init__(self, size=Optional[int]):
        self.layers: Dict[int, MapLayer] = {}
        self.size = size

    def add_layer(self, layer: MapLayer, elevation: int):
        if isinstance(self.size, int) and elevation >= self.size:
            raise IndexError(
                f"Could not add layer to bounded level of size {self.size} at elevation {elevation}"
            )
        else:
            self.layers[elevation] = layer

    def get_layer(self, elevation: int) -> Optional[MapLayer]:
        try:
            layer = self.layers[elevation]
            return layer
        except KeyError:
            return None

    def __str__(self) -> str:
        repr = ""
        for e, layer in self.layers.items():
            repr += f"Elevation {e}:\n"
            repr += str(layer)

        return repr
