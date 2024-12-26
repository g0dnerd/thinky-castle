from game.level import Layer, Level, Square
from game.props import Ladder

from render.render import game_loop

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600


def layer_test(lvl: Level):
    ml = Layer(5)
    lvl.add_layer(ml, 1)
    print(lvl)

    layer = lvl.get_layer(1)
    assert layer

    print("Adding a wall between E4 and E5.")
    layer.add_wall(Square.from_name("E4"), Square.from_name("E5"))
    print(lvl)

    print("Adding a wall between E4 and D4.")
    layer.add_wall(Square.from_name("E4"), Square.from_name("D4"))
    print(lvl)

    print("Adding a ladder on A2.")
    ladder = Ladder()
    layer.add_prop(Square.from_name("A2"), ladder)
    print(lvl)


def main():
    lvl = Level()
    ml = Layer(5)
    lvl.add_layer(ml, 1)

    layer_test(lvl)

    game_loop(DISPLAY_WIDTH, DISPLAY_HEIGHT, lvl)


if __name__ == "__main__":
    main()
