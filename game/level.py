from enum import Enum
from typing import Dict, Optional

from game.props import Prop


class Direction(Enum):
    """Movement directions in x/z space"""

    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)


class Square:
    """Represents a node index in x/y space.
    A1 is (0, 0), A2 is (0, 1), E5 is (4, 4).
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

        return cls(file_idx, rank_idx)

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
        """Adds the target node as the connected node for the specified direction."""
        self.connected_nodes[dir] = target

    def is_accessible(self, dir):
        """If there is a connected node in the specified direction,
        returns it and false otherwise.
        """
        return self.connected_nodes.get(dir, False)

    def add_prop(self, prop: Prop):
        if not self.prop:
            self.prop = prop
        else:
            raise ValueError("Can't add prop to occupied node.")


class Layer:
    def __init__(self, size: int):
        """Creates a new square map layer of size x."""
        self.size = size

        # Initialize a two-dimensional list of empty nodes
        self.nodes = [[Node(Square(x, y)) for y in range(size)] for x in range(size)]
        self.connect_nodes()

    def connect_nodes(self):
        """Automatically connects adjacent nodes to each other."""
        for x in range(self.size):
            for y in range(self.size):
                node = self.get_node(Square(x, y))
                assert node, f"Expected node in map layer at {x}, {y}, but got None."

                for dir in Direction:
                    dx = dir.value[0]
                    dy = dir.value[1]

                    # Try to get the neightbor in the given direction
                    neighbor = self.get_node(Square(x + dx, y + dy))
                    if neighbor:
                        # If one exists, connect it to the current node.
                        node.connect(dir, neighbor)

    def add_wall(self, a: Square, b: Square):
        """Adds a wall, e.g. removes the connection between two nodes."""
        node1 = self.get_node(a)
        node2 = self.get_node(b)
        assert node1 and node2, f"Could not find nodes to connect at {a} and {b}."

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
        cols = []

        file_labels = " "
        # Add rank indices
        for i in range(self.size):
            file_labels += f"{i + 1} "

        file_labels = file_labels.removesuffix(" ")
        cols.append(file_labels)

        for x, row in enumerate(self.nodes):
            # Add file indices
            horizontal_walls = " "
            col = f"{chr(ord("A") + x)}"
            for y, node in enumerate(row):
                col += "o" if not node.prop else str(node.prop)
                if y < self.size - 1:
                    col += " " if node.is_accessible(Direction.DOWN) else "-"
                if x < self.size - 1:
                    horizontal_walls += (
                        "  " if node.is_accessible(Direction.RIGHT) else "| "
                    )

            col = col.removesuffix(" ")
            cols.append(col)
            if horizontal_walls and x < self.size - 1:
                cols.append(horizontal_walls)

        repr = ""
        for x in range(self.size * 2):
            for c in cols:
                repr += c[x] + " "
            repr += "\n"

        return repr


class Level:
    """Holds any number of vertically arranged map layers."""

    def __init__(self, size=Optional[int]):
        """Initializes a map with layers stored in a dictionary[elevation, Layer].
        You can optionally specify a maximum size for this level.
        """
        self.layers: Dict[int, Layer] = {}
        self.size = size

    def add_layer(self, layer: Layer, elevation: int):
        """Adds a layer to the level at the given elevation."""
        if isinstance(self.size, int) and elevation >= self.size:
            raise IndexError(
                f"Could not add layer to bounded level of size {self.size} at elevation {elevation}"
            )
        else:
            if elevation in self.layers:
                raise ValueError(
                    f"Could not add level at elevation {elevation} because it is occupied."
                )
            self.layers[elevation] = layer

    def get_layer(self, elevation: int) -> Optional[Layer]:
        """Returns the layer at the given elevation if it exists and None otherwise."""
        return self.layers.get(elevation)

    def __str__(self) -> str:
        repr = ""
        for e, layer in self.layers.items():
            repr += f"Elevation {e}:\n"
            repr += str(layer)

        return repr
