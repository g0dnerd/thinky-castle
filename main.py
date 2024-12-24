from game.map import MapLayer, Square
from game.props import Ladder


def main():
    ml = MapLayer(5)
    print(str(ml))

    print("Adding a wall between E4 and E5.")
    ml.add_wall(Square.from_name("E4"), Square.from_name("E5"))
    print(str(ml))

    print("Adding a wall between E4 and D4.")
    ml.add_wall(Square.from_name("E4"), Square.from_name("D4"))
    print(str(ml))

    print("Adding a ladder on A2.")
    ladder = Ladder()
    ml.add_prop(Square.from_name("A2"), ladder)
    print(ml)


if __name__ == "__main__":
    main()
