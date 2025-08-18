from animals import Animal
from toolbox import scroll
from player import Player
from random import choice
import sys


class InputHandler:
    def __init__(self, player: Player):
        self.player = player

    def decide_add_willing(self, willing_animals: list[Animal]) -> Animal | None:
        """
        Prompts user to choose (or not choose) one willing animal to join the team.

        Returns:
            The Animal the player chose, or None
        """
        idx = self.get_choice(willing_animals + ["I don't want these ones"])

        # "I don't want these ones" option
        if idx == len(willing_animals):
            scroll(f"* {choice(willing_animals)} felt rejected")  # TODO: Randomize this line
            return None

        return willing_animals[idx]

    def decide_targets(self, my_animals: list[Animal], enemy_animals: list[Animal]):
        """
        Prompts the user to select attack targets for each of their Animals.

        Parameters:
            my_animals (list[Animal]): The player's Animals.
            enemy_animals (list[Animal]): The enemy Animals.
        """
        for my_animal in my_animals:
            scroll()
            scroll(f"* Choose which animal your {my_animal} targets")

            # Allow Animals not to attack
            idx = self.get_choice(enemy_animals + ["Don't attack"])
            if idx < len(enemy_animals):
                my_animal.set_target(enemy_animals[idx])

    def get_choice(self, options: list) -> int:
        """
        Given a list of options to choose from, return the index of the selected choice.
        """
        idx = -1
        input_str = ""

        for i, option in enumerate(options):
            input_str += f"{i+1}. {option}\n"
        scroll(input_str, end="")

        while idx < 0:
            inp = input(">> ").strip()

            # Check for quit
            if inp == "q":
                sys.exit()

            # View party option
            if inp == "v":
                self.player.print_party()
                continue

            # Check is number
            if not inp.isnumeric():
                print("! Please input one of the option numbers")
                continue
            inp = int(inp)

            # Check number within the range of options and viewing the player's party
            if inp < 1 or inp > len(options) + 1:
                print("! Please input one of the option numbers")
                continue

            # Convert number to index
            idx = inp - 1

        return idx
