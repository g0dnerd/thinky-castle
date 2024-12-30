from game.level import Direction, Layer, Level

PATH_COLOR = (1, 1, 1)
WALL_COLOR = (1, 0, 0.3)
BOUNDARY_COLOR = (0, 0, 1)

GRID_SPACING = 2


def make_level_mesh(lvl: Level):
    """Convert a level's structure into OpenGL vertices, edges, and colors."""
    edges = []
    vertices = []
    colors = []

    def layer_boundaries(layer: Layer, e: int):
        """Makes a list of 4 (x, y, z) tuples for the boundary vertices of the given layer."""
        size = layer.size
        vertices.extend(
            [
                (-size, e, size),
                (-size, e, -size),
                (size, e, size),
                (size, e, -size),
            ]
        )
        edges.extend([(0, 1), (0, 2), (1, 3), (2, 3)])
        colors.extend([BOUNDARY_COLOR] * 4)

    def make_grid(layer: Layer, e: int):
        """Computes vertices, edges and colors for all grid lines and wall segments
        in the given layer.
        """
        size = layer.size

        for idx in range(1, size):
            # End points for horizontal grid line
            h1 = (-size, e, idx * GRID_SPACING - size)
            h2 = (size, e, idx * GRID_SPACING - size)

            # End points for vertical grid line
            v1 = (idx * GRID_SPACING - size, e, -size)
            v2 = (idx * GRID_SPACING - size, e, size)

            vertices.extend([h1, h2, v1, v2])
            offset = len(vertices)
            edges.append((offset - 4, offset - 3))
            edges.append((offset - 2, offset - 1))
            colors.extend([PATH_COLOR] * 2)

    def make_colors(layer: Layer, e: int):
        """Colors each edge segment between two nodes with WALL_COLOR if there is a wall there."""
        size = layer.size

        for rank in layer.nodes:
            for node in rank:
                x = node.pos.x
                y = node.pos.y

                if 0 < x < size - 1:
                    if not node.is_accessible(Direction.RIGHT):
                        p1 = pos_to_coords(x + 1, y, size, e)
                        p2 = pos_to_coords(x + 1, y + 1, size, e)
                        vertices.extend([p1, p2])
                        offset = len(vertices)
                        edges.append((offset - 2, offset - 1))
                        colors.append(WALL_COLOR)

                if 0 < y < size - 1:
                    if not node.is_accessible(Direction.DOWN):
                        p1 = pos_to_coords(x, y + 1, size, e)
                        p2 = pos_to_coords(x + 1, y + 1, size, e)
                        vertices.extend([p1, p2])
                        offset = len(vertices)
                        edges.append((offset - 2, offset - 1))
                        colors.append(WALL_COLOR)

    for elevation, layer in lvl.layers.items():
        layer_boundaries(layer, elevation)
        make_grid(layer, elevation)
        make_colors(layer, elevation)

    return vertices, edges, colors


def pos_to_coords(x: int, y: int, size: int, e: int):
    """Returns the vertex coordinates of the top left corner of the given square."""
    return (x * GRID_SPACING - size, e, y * GRID_SPACING - size)
