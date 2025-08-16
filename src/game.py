from input_handler import InputHandler
from ai_handler import AIHandler
from player import Player
from animals import *
from toolbox import *


class Game:
    def __init__(self):
        # Objects
        self.ai_handler = AIHandler()
        self.player = Player()
        self.input_handler = InputHandler(self.player)

        # Settings
        self.running = False
        self.n_battles = 5

    def _enter_training(self):
        print()
        iprint("* Choose an animal to train")
        self.player.reset_animal_stats()
        self.player.decide_training_buffs()
        self.player.train_animal(self.input_handler.get_choice(self.player.party))

    def _enter_battle(self, boss=False):
        self.n_battles -= 1

        if boss:
            self.ai_handler.boss_party()
        else:
            self.ai_handler.randomize_party()
        self.player.reset_animal_stats()

        print()
        print(f"~ {self.n_battles if not boss else "BOSS"} ~")
        iprint("* You encountered:")
        for animal in self.ai_handler.party:
            iprint(f"- A {animal}")

        # Create queue from highest speed to lowest speed
        qq: list[Animal] = self.player.party + self.ai_handler.party
        qq.sort(key=lambda x: x.spd, reverse=True)

        while True:
            # Decide wild animals willing to joing player if player has room
            willing_animals = self.ai_handler.get_willing_animals()
            if len(willing_animals) > 0:
                print()
                iprint("* Some of the wild beasts seemed willing to join your party")
                if self.player.has_full_party():
                    iprint("* But your party was full")
                else:
                    print()
                    iprint("* Choose which animal joins you")
                    added = self.input_handler.decide_add_willing(willing_animals)
                    if added:
                        self.ai_handler.remove_animal(added)
                        self.player.add_animal(added)
                        if self.ai_handler.all_animals_dead():
                            print()
                            iprint("* Fearing your wrath and comforted by your demeanor, the wild animals followed you")
                            return

            # Decide targets
            player_animals = self.player.animals_that_can_attack()
            wild_animals = self.ai_handler.animals_that_can_be_attacked()
            self.input_handler.decide_targets(player_animals, wild_animals)

            player_animals = self.player.animals_that_can_be_attacked()
            wild_animals = self.ai_handler.animals_that_can_attack()
            self.ai_handler.decide_targets(wild_animals, player_animals)

            # Execute actions
            for animal in qq:
                animal.execute_action()

            # Remove dead animals from the game
            self.player.remove_dead_animals()
            self.ai_handler.remove_dead_animals()
            remove_dead_animals(qq)

            # Check for win/loss
            if self.player.all_animals_dead():
                self._handle_player_loss()
                return
            if self.ai_handler.all_animals_dead():
                self._handle_player_win()
                return

    def _handle_player_loss(self):
        print()
        iprint("* All your Animals died")
        iprint("* Unprotected, you fell prey to a swarm of angry squirrels")  # TODO: Randomize this line
        self.running = False

    def _handle_player_win(self):
        print()
        iprint("* The wild beasts fled from your animals' ruthless attacks")  # TODO: Randomize this

    def start(self):
        self.running = True

        print()
        iprint("* Choose your starting companion")
        start_options = [Hound(), Cat()]
        self.player.add_animal(start_options[self.input_handler.get_choice(start_options)])

        # General battles
        while self.player.is_alive() and self.n_battles > 0:
            self._enter_battle()
            if self.player.is_alive():
                self._enter_training()

        # Boss battle
        if self.player.is_alive():
            self._enter_battle(boss=True)
