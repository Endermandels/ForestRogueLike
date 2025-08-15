from input_handler import InputHandler
from ai_handler import AIHandler
from player import Player
from animals import *
from toolbox import *

class Game:
    def __init__(self):
        self.input_handler = InputHandler()
        self.ai_handler = AIHandler()
        self.player = Player()
    
    def _randomize_encounter(self) -> list[Animal]:
        '''
        Return a list of up to 3 animals for the encounter.
        '''
        return [Hound(), Cat()] # TODO: Fix this
    
    def _enter_training(self):
        pass
    
    def _enter_battle(self):
        wild_animals = self._randomize_encounter()
        
        # Create queue from highest speed to lowest speed
        qq: list[Animal] = (self.player.party + wild_animals)
        qq.sort(key=lambda x: x.spd, reverse=True)
        
        while True:
            # Decide targets
            self.input_handler.decide_targets(filter_can_attack(self.player.party), filter_can_be_attacked(wild_animals))
            self.ai_handler.decide_targets(filter_can_attack(wild_animals), filter_can_be_attacked(self.player.party))
            
            # Execute actions
            for animal in qq:
                animal.execute_action()
            
            # Check for winner/loser
            if all_animals_dead(self.player.party):
                self._handle_player_loss()
                return
            if all_animals_dead(wild_animals):
                self._handle_player_win()
                return
            
            # Remove dead animals from the queue
            remove_dead_animals(qq)
                
    def _handle_player_loss(self):
        print("* All your Animals died")
        print("* Unprotected, you fell prey to a swarm of angry squirrels") # TODO: Randomize this line
        
    def _handle_player_win(self):
        print("* The wild beasts fled from your animals' ruthless attacks") # TODO: Randomize this line
    
    def start(self):
        print("* Choose your starting companion:")
        start_options = [Hound(), Cat()]
        self.player.add_animal(start_options[self.input_handler.get_choice(start_options)])
        self._enter_battle()
        