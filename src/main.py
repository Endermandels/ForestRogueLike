from game import Game
from toolbox import scroll


def main():
    scroll("~~~ FOREST ROGUE LIKE ~~~")

    cur_game = Game()
    cur_game.start()

    scroll("~ Come Again Soon ~")


if __name__ == "__main__":
    main()
