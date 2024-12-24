from game import map
from game.props import Ladder


def main():
    lvl = map.Level()
    ml = map.MapLayer(5)
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


if __name__ == "__main__":
    main()
