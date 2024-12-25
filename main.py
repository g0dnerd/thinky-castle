from game import map
from game.props import Ladder

from render.render import game_loop

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

SURFACES = [
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6),
]

# Location of each vertex in the X, Y, Z plane
VERTICES = [
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
]

# Indices of the vertices between which the edge will be drawn
EDGES = [
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
]


def layer_test():
    lvl = map.Level()
    ml = map.Layer(5)
    lvl.add_layer(ml, 1)
    print(lvl)

    layer = lvl.get_layer(1)
    assert layer

    print("Adding a wall between E4 and E5.")
    layer.add_wall(map.Square.from_name("E4"), map.Square.from_name("E5"))
    print(lvl)

    print("Adding a wall between E4 and D4.")
    layer.add_wall(map.Square.from_name("E4"), map.Square.from_name("D4"))
    print(lvl)

    print("Adding a ladder on A2.")
    ladder = Ladder()
    layer.add_prop(map.Square.from_name("A2"), ladder)
    print(lvl)


def main():
    # layer_test()
    level = map.Level()
    ml = map.Layer(5)
    level.add_layer(ml, 1)
    game_loop(DISPLAY_WIDTH, DISPLAY_HEIGHT, level)


if __name__ == "__main__":
    main()
