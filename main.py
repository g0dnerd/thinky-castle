from game.map import MapLayer, Square


def main():
    ml = MapLayer(5)
    print(str(ml))

    print("Adding a wall between E4 and E5.")
    ml.add_wall(Square(3, 4), Square(4, 4))
    print(str(ml))

    print("Adding a wall between E4 and D4.")
    ml.add_wall(Square(3, 4), Square(3, 3))
    print(str(ml))


if __name__ == "__main__":
    main()
