'''
Stats breakdown:
    HP: 1-6
    ATK: 1-4
    SPD: 1-3
'''

from enum import Enum

class Action(Enum):
    TARGET = 'target'

class Animal:
    def __init__(self, hp, atk, spd, name="Animal"):
        self.name = name
        self.max_hp = hp
        self.hp = self.max_hp
        self.atk = atk
        self.spd = spd
        
        self.action = {}
    
    def __repr__(self) -> str:
        return f'{self.name}: [{self.hp}] [{self.atk}] [{self.spd}]'
    
    def set_target(self, target):
        '''
        target: Animal
        '''
        self.action[Action.TARGET] = target
    
class Hound(Animal):
    def __init__(self, hp=2, atk=2, spd=2):
        Animal.__init__(self, hp, atk, spd, name="Hound")

class Cat(Animal):
    def __init__(self, hp=3, atk=1, spd=3):
        Animal.__init__(self, hp, atk, spd, name="Cat")
        