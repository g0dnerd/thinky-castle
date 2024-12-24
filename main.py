from game.map import MapLayer, Square


def main():
    ml = MapLayer(5)
    print(str(ml))

    print("Adding a wall between E4 and E5.")
    ml.add_wall(Square.from_name("E4"), Square.from_name("E5"))
    print(str(ml))

    print("Adding a wall between E4 and D4.")
    ml.add_wall(Square.from_name("E4"), Square.from_name("D4"))
    print(str(ml))


if __name__ == "__main__":
    main()
