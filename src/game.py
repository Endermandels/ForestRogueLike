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

    def _enter_training(self):
        print("* Choose an animal to train")
        self.player.reset_animal_stats()
        self.player.decide_training_buffs()
        self.player.train_animal(self.input_handler.get_choice(self.player.party))

    def _enter_battle(self):
        self.n_battles -= 1
        self.ai_handler.randomize_party()
        self.player.reset_animal_stats()

        print()
        print("* You encountered:")
        for animal in self.ai_handler.party:
            print(f"- A {animal}")

        # Create queue from highest speed to lowest speed
        qq: list[Animal] = self.player.party + self.ai_handler.party
        qq.sort(key=lambda x: x.spd, reverse=True)

        while True:
            # Decide targets
            self.input_handler.decide_targets(
                self.player.animals_that_can_attack(), self.ai_handler.animals_that_can_be_attacked()
            )
            self.ai_handler.decide_targets(
                self.ai_handler.animals_that_can_attack(), self.player.animals_that_can_be_attacked()
            )

            # Execute actions
            for animal in qq:
                if not animal.is_dead():
                    animal.execute_action()
                    input()  # TODO: Make it so that only when text appears this input is activated

            # Remove dead animals from the game
            self.player.remove_dead_animals()
            self.ai_handler.remove_dead_animals()

            # Check for win/loss
            if self.player.all_animals_dead():
                self._handle_player_loss()
                return
            if self.ai_handler.all_animals_dead():
                self._handle_player_win()
                return

    def _handle_player_loss(self):
        print()
        print("* All your Animals died")
        print("* Unprotected, you fell prey to a swarm of angry squirrels")  # TODO: Randomize this line
        print()
        self.running = False

    def _handle_player_win(self):
        print()
        print("* The wild beasts fled from your animals' ruthless attacks")  # TODO: Randomize this
        print()

    def start(self):
        self.running = True

        print("* Choose your starting companion")
        start_options = [Hound(), Cat()]
        self.player.add_animal(start_options[self.input_handler.get_choice(start_options)])

        while self.running:
            self._enter_battle()
            if self.running:
                self._enter_training()
