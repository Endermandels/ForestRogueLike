from input_handler import InputHandler
from ai_handler import AIHandler
from player import Player
from animals import *
from toolbox import *


class Game:
    def __init__(self):
        # Objects
        self.input_handler = InputHandler()
        self.ai_handler = AIHandler()
        self.player = Player()

        # Settings
        self.running = False
        self.n_battles = 5

    def _randomize_encounter(self) -> list[Animal]:
        """
        Return a list of up to 3 animals for the encounter.
        """
        return [Hound()]  # TODO: Fix this

    def _enter_training(self):
        print("* Choose an animal to train")

    def _enter_battle(self):
        self.n_battles -= 1
        wild_animals = self._randomize_encounter()

        print()
        print("* You encountered:")
        for animal in wild_animals:
            print(f"- A {animal}")

        # Create queue from highest speed to lowest speed
        qq: list[Animal] = self.player.party + wild_animals
        qq.sort(key=lambda x: x.spd, reverse=True)

        while True:
            # Decide targets
            self.input_handler.decide_targets(
                filter_can_attack(self.player.party), filter_can_be_attacked(wild_animals)
            )
            self.ai_handler.decide_targets(filter_can_attack(wild_animals), filter_can_be_attacked(self.player.party))

            # Execute actions
            for animal in qq:
                animal.execute_action()

            # Remove dead animals from the game
            remove_dead_animals(self.player.party)
            remove_dead_animals(wild_animals)

            # Check for win/loss
            if len(self.player.party) < 1:
                self._handle_player_loss()
                return
            if len(wild_animals) < 1:
                self._handle_player_win()
                return

    def _handle_player_loss(self):
        print("* All your Animals died")
        print("* Unprotected, you fell prey to a swarm of angry squirrels")  # TODO: Randomize this line
        self.running = False

    def _handle_player_win(self):
        print("* The wild beasts fled from your animals' ruthless attacks")  # TODO: Randomize this

    def start(self):
        self.running = True

        print("* Choose your starting companion")
        start_options = [Hound(), Cat()]
        self.player.add_animal(start_options[self.input_handler.get_choice(start_options)])

        while self.running:
            self._enter_battle()
            if self.running:
                self._enter_training()
