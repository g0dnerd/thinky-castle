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
        """Adds boundary vertices and edges for a layer."""
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
        """Adds grid vertices and checks for walls."""
        size = layer.size
        for x in range(-size, size + GRID_SPACING, GRID_SPACING):
            for z in range(-size, size + GRID_SPACING, GRID_SPACING):
                if abs(x) == size and abs(z) == size:  # Skip corner vertices
                    continue
                vertices.append((x, e, z))

        for a, v1 in enumerate(vertices):
            for b, v2 in enumerate(vertices):
                if a >= b:  # Avoid redundant checks
                    continue
                if (a, b) in edges or (b, a) in edges:  # Skip existing edges
                    continue

                ax, _, az = v1
                bx, _, bz = v2

                # Check if nodes are adjacent
                if abs(ax - bx) == GRID_SPACING and az == bz:  # Horizontal adjacency
                    add_wall_or_path(layer, a, b, ax, bx, az, True)
                elif abs(az - bz) == GRID_SPACING and ax == bx:  # Vertical adjacency
                    add_wall_or_path(layer, a, b, az, bz, ax, False)

    def add_wall_or_path(layer, a, b, coord1, coord2, fixed_coord, is_horizontal):
        """Adds walls or paths between adjacent nodes."""
        size = layer.size

        # If a path lies on the level boundary, it can't be a wall
        if abs(fixed_coord) == size:
            colors.append(BOUNDARY_COLOR)
            edges.append((a, b))
            return

        # Determine the shared coordinate from the left/upper point of the path
        match min(coord1, coord2):
            case -5:
                fixed = 0
            case -3:
                fixed = 1
            case -1:
                fixed = 2
            case 1:
                fixed = 3
            case 3:
                fixed = 4
            case _:
                raise ValueError

        # Determine the middle coordinate from the shared coordinate of the path
        match fixed_coord:
            case -3:
                mid = 0
            case -1:
                mid = 1
            case 1:
                mid = 2
            case 3:
                mid = 3
            case _:
                raise ValueError

        if is_horizontal:
            sq_a = Square(fixed, mid)
            sq_b = Square(fixed, mid + 1)
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
                colors.append(WALL_COLOR)  # Wall
            else:
                colors.append(PATH_COLOR)  # Path
            edges.append((a, b))

    for e, layer in enumerate(lvl.layers.values()):
        add_boundary(layer, e)
        add_grid_lines(layer, e)

    return vertices, edges, colors
