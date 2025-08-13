from animals import Animal
from random import choice

class AIHandler:
    '''
    Acts as an opponent would act IRL
    '''
    
    def __init__(self):
        pass
    
    def decide_targets(self, my_animals: list[Animal], enemy_animals: list[Animal]):
        '''
        Decide which animals attack which opponents
        '''
        for my_animal in my_animals:
            my_animal.set_target(choice(enemy_animals))