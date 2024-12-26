from game.level import Level, Square

PATH_COLOR = (1, 1, 1)
WALL_COLOR = (1, 0, 0.7)
BOUNDARY_COLOR = (0, 0, 1)

GRID_SPACING = 2


def make_level_mesh(lvl: Level):
    """Convert a level's structure into OpenGL vertices, edges, and colors."""
    vertices = []
    edges = []
    colors = []

    def add_boundary(layer, e):
        """Adds boundary vertices and edges for a layer, e.g. the four bounding walls."""
        size = layer.size
        boundary_vertices = [
            (size, e, -size),
            (-size, e, -size),
            (size, e, size),
            (-size, e, size),
        ]
        vertices.extend(boundary_vertices)

        o = len(vertices) - len(
            boundary_vertices
        )  # Offset for current layer's boundaries

        boundary_edges = [
            (0 + o, 1 + o),
            (0 + o, 2 + o),
            (1 + o, 3 + o),
            (2 + o, 3 + o),
        ]
        edges.extend(boundary_edges)
        colors.extend([BOUNDARY_COLOR] * len(boundary_edges))

    def add_grid_lines(layer, e):
        """Adds grid vertices and checks for walls between nodes, coloring them accordingly."""
        size = layer.size

        # Add a vertex segment for each node corner
        for x in range(-size, size + GRID_SPACING, GRID_SPACING):
            for z in range(-size, size + GRID_SPACING, GRID_SPACING):
                if (
                    abs(x) == size and abs(z) == size
                ):  # We already added corner vertices
                    continue

                vertices.append((x, e, z))

        # Add an edge between all adjacent vertices
        for a, v1 in enumerate(vertices):
            for b, v2 in enumerate(vertices):
                if a >= b or (a, b) in edges or (b, a) in edges:  # Skip existing edges
                    continue

                ax, _, az = v1
                bx, _, bz = v2

                # Check if vertices are adjacent
                if abs(ax - bx) == GRID_SPACING and az == bz:  # Horizontal adjacency
                    add_wall_or_path(layer, a, b, ax, bx, az, True)
                elif abs(az - bz) == GRID_SPACING and ax == bx:  # Vertical adjacency
                    add_wall_or_path(layer, a, b, az, bz, ax, False)

    def add_wall_or_path(layer, a, b, coord1, coord2, fixed_coord, is_horizontal):
        """Adds edges between two adjacent vertices and checks if they are walls or not."""
        size = layer.size

        # If a path lies on a level boundary edge, it can't be a wall
        if abs(fixed_coord) == size:
            colors.append(BOUNDARY_COLOR)
            edges.append((a, b))
            return

        # Determine the shared coordinate from the leftmost/highest point of the path
        fixed = (min(coord1, coord2) + size) // 2

        # Determine the middle coordinate from the shared coordinate of the path
        mid = (fixed_coord + size - GRID_SPACING) // GRID_SPACING

        # If the edge is horizontal, that means the nodes are one vertical space apart
        if is_horizontal:
            sq_a = Square(fixed, mid)
            sq_b = Square(fixed, mid + 1)

        # If the edge is vertical, that means the nodes are one horizontal space apart
        else:
            sq_a = Square(mid, fixed)
            sq_b = Square(mid + 1, fixed)

        node_a = layer.get_node(sq_a)
        node_b = layer.get_node(sq_b)

        if node_a and node_b:
            if (
                node_b not in node_a.connected_nodes.values()
                and node_a not in node_b.connected_nodes.values()
            ):
                colors.append(WALL_COLOR)
            else:
                colors.append(PATH_COLOR)

            edges.append((a, b))

    for e, layer in enumerate(lvl.layers.values()):
        add_boundary(layer, e)
        add_grid_lines(layer, e)

    return vertices, edges, colors
