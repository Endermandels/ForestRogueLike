from input_handler import InputHandler
from ai_handler import AIHandler
from player import Player
from animals import *

class Game:
    def __init__(self):
        self.input_handler = InputHandler()
        self.ai_handler = AIHandler()
        self.player = Player()
    
    def _randomize_encounter(self) -> list[Animal]:
        '''
        Return a list of up to 3 animals for the encounter.
        '''
        return [Hound()] # TODO: Fix this
    
    def _enter_training(self):
        pass
    
    def _enter_battle(self):
        wild_animals = self._randomize_encounter()
        
        # Create queue from highest speed to lowest speed
        qq = (wild_animals + self.player.party)
        qq.sort(key=lambda x: x.spd, reverse=True)
        
        while True:
            self.input_handler.decide_targets(self.player.party, wild_animals)
            self.ai_handler.decide_targets(wild_animals, self.player.party)
            break
    
    def start(self):
        print("* Choose your starting companion:")
        
        start_options = [Hound(), Cat()]
        self.player.add_animal(start_options[self.input_handler.get_choice(start_options)])
        self._enter_battle()
        