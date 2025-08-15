'''
Stats breakdown:
    HP: 1-6
    ATK: 1-4
    SPD: 1-3
'''

from toolbox import clamp
from enum import Enum

class Action(Enum):
    ATTACK = 'attack'

class Animal:
    def __init__(self, hp: int, atk: int, spd: int, is_wild: bool=True, name: str="Animal"):
        self.name = name
        self.is_wild = is_wild
        self.max_hp = hp
        self.hp = self.max_hp
        self.atk = atk
        self.spd = spd
        
        self.action = {}
    
    def __repr__(self) -> str:
        return f'{'Wild' if self.is_wild else 'Tamed'} {self.name} [{self.hp}]: [{self.atk}] [{self.spd}]'
    
    def set_target(self, target):
        '''
        target: Animal
        '''
        self.action[Action.ATTACK] = target
    
    def execute_action(self):
        # Can't execute action if already dead
        if self.is_dead():
            return
        
        if Action.ATTACK in self.action:
            enemy: Animal = self.action[Action.ATTACK]
            print(f'{self} attacked {enemy}')
            enemy.take_dmg(self, self.atk)
        
        # Reset stored action
        self.action = {}
    
    def take_dmg(self, enemy, amount: int):
        # Can't take damage if already dead
        if self.is_dead():
            return
        
        old_hp = self.hp
        self.hp = clamp(self.hp - amount, 0, self.max_hp)
        print(f'{self} took {old_hp - self.hp} damage')

        if self.is_dead():
            print(f'### {self} died!')
    
    def is_dead(self) -> bool:
        return self.hp <= 0
    
    def can_attack(self) -> bool:
        return not self.is_dead()
    
    def can_be_attacked(self) -> bool:
        return not self.is_dead()
    
    def tame(self):
        self.is_wild = False
    
class Hound(Animal):
    def __init__(self, hp: int=2, atk: int=2, spd: int=2, is_wild: bool=True):
        Animal.__init__(self, hp, atk, spd, is_wild=is_wild, name="Hound")

class Cat(Animal):
    def __init__(self, hp: int=3, atk: int=1, spd: int=3, is_wild: bool=True):
        Animal.__init__(self, hp, atk, spd, is_wild=is_wild, name="Cat")
        