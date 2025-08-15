"""
Stats breakdown:
    HP: 1-6
    ATK: 1-4
    SPD: 1-3
"""

from __future__ import annotations
from random import randint
from toolbox import clamp
from enum import Enum


# Animal Actions
class Action(Enum):
    ATTACK = "attack"


# Training Buffs
class Buff(Enum):
    ATK = "ATK"
    HP = "HP"
    NONE = ""


class Animal:
    def __init__(self, hp: int, atk: int, spd: int, is_wild: bool = True, name: str = "Animal"):
        self.name = name
        self.is_wild = is_wild
        self.max_hp = hp
        self.hp = self.max_hp
        self.atk = atk
        self.spd = spd

        self.action = {}
        self.training_buff = Buff.NONE

    def __repr__(self) -> str:
        return (
            f"{'Wild' if self.is_wild else 'Tamed'}"
            f" {self.name}"
            f" ({self.hp}{' + 2' if self.training_buff == Buff.HP else ''}):"
            f" [{self.atk}{' + 1' if self.training_buff == Buff.ATK else ''}]"
            f" [{self.spd}]"
        )

    def set_target(self, target: Animal):
        self.action[Action.ATTACK] = target

    def execute_action(self):
        # Can't execute action if already dead
        if self.is_dead():
            return

        if Action.ATTACK in self.action:
            enemy: Animal = self.action[Action.ATTACK]
            if enemy.can_be_attacked():
                print(f"! {self} attacked {enemy}")
                enemy.take_dmg(self, self.atk)

        # Reset stored action
        self.action = {}

    def take_dmg(self, enemy: Animal, amount: int):
        # Can't take damage if already dead
        if self.is_dead():
            return

        old_hp = self.hp
        self.hp = clamp(self.hp - amount, 0, self.max_hp)
        print(f"! {self} took {old_hp - self.hp} damage")

        if self.is_dead():
            print(f"! {self} died")

    def is_dead(self) -> bool:
        return self.hp <= 0

    def can_attack(self) -> bool:
        return not self.is_dead()

    def can_be_attacked(self) -> bool:
        return not self.is_dead()

    def tame(self):
        self.is_wild = False

    def decide_training_buff(self):
        buff_type = randint(0, 1)
        if buff_type == 0:
            self.training_buff = Buff.ATK
        elif buff_type == 1:
            self.training_buff = Buff.HP

    def train(self):
        if self.training_buff == Buff.ATK:
            self.atk += 1
        if self.training_buff == Buff.HP:
            self.max_hp += 2

    def clear_training_buff(self):
        self.training_buff = Buff.NONE

    def reset_stats(self):
        self.hp = self.max_hp


class Hound(Animal):
    def __init__(self, hp: int = 2, atk: int = 2, spd: int = 2, is_wild: bool = True):
        Animal.__init__(self, hp, atk, spd, is_wild=is_wild, name="Hound")


class Cat(Animal):
    def __init__(self, hp: int = 3, atk: int = 1, spd: int = 3, is_wild: bool = True):
        Animal.__init__(self, hp, atk, spd, is_wild=is_wild, name="Cat")
