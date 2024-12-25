from game.map import Level


def prerender_level(level: Level):
    vertices = []
    edges = []

    for e, layer in enumerate(level.layers.values()):
        vertices.append((layer.size, e, -layer.size))
        vertices.append((-layer.size, e, -layer.size))
        vertices.append((layer.size, e, layer.size))
        vertices.append((-layer.size, e, layer.size))

        o = e * 4  # Offset in the lists of matrices
        edges.extend([(0 + o, 1 + o), (0 + o, 2 + o), (1 + o, 3 + o), (2 + o, 3 + o)])

        for i in range(layer.size - 1):
            x = -layer.size + 2 + 2 * i
            vertices.append((x, e, -layer.size))
            vertices.append((x, e, layer.size))
            e_o = 4 + o + i * 4
            edges.append((e_o, e_o + 1))

            vertices.append((-layer.size, e, x))
            vertices.append((layer.size, e, x))
            edges.append((e_o + 2, e_o + 3))

    return (
        vertices,
        edges,
    )
