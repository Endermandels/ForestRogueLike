from __future__ import annotations
from random import randint
from toolbox import clamp, iprint
from enum import Enum
from colorama import Fore, Style


# Animal Actions
class Action(Enum):
    ATTACK = "attack"


# Training Buffs
class Buff(Enum):
    ATK = "ATK"
    HP = "HP"
    NONE = ""


class Animal:
    def __init__(self, hp: int, atk: int, spd: int, friendliness: int, is_wild: bool = True, name: str = "Animal"):
        """
        Stats breakdown:
            HP (health points): 1-6
            ATK (attack): 1-4
            SPD (speed): 1-3
            FRE (friendliness): 1-5
        """
        self.name = name
        self.is_wild = is_wild
        self.max_hp = hp
        self.hp = self.max_hp
        self.atk = atk
        self.spd = spd
        self.friendliness = friendliness

        self.action = {}
        self.training_buff = Buff.NONE

    def __repr__(self) -> str:
        return (
            f"{Fore.RED + 'Wild' if self.is_wild else Fore.GREEN + 'Tamed'}"
            f" {self.name}{Style.RESET_ALL}"
            f" ({self.hp}{Fore.YELLOW + ' +2' + Style.RESET_ALL if self.training_buff == Buff.HP else ''}):"
            f" [{self.atk}{Fore.YELLOW + ' +1' + Style.RESET_ALL if self.training_buff == Buff.ATK else ''}]"
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
                iprint(f"! {self} attacked {enemy}")
                enemy.take_dmg(self, self.atk)

        # Reset stored action
        self.action = {}

    def take_dmg(self, enemy: Animal, amount: int):
        # Can't take damage if already dead
        if self.is_dead():
            return

        old_hp = self.hp
        self.hp = clamp(self.hp - amount, 0, self.max_hp)
        iprint(f"! {self} took {Fore.YELLOW}{old_hp - self.hp}{Style.RESET_ALL} damage")

        if self.is_dead():
            iprint(f"! {self} {Fore.RED}died{Style.RESET_ALL}")

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
            self.training_buff = Buff.NONE
            iprint(f"$ Your {self} increased its ATK")
            self.atk += 1
        if self.training_buff == Buff.HP:
            self.training_buff = Buff.NONE
            iprint(f"$ Your {self} increased its HP")
            self.max_hp += 2

    def clear_training_buff(self):
        self.training_buff = Buff.NONE

    def reset_stats(self):
        self.hp = self.max_hp

    def is_willing_to_join_player(self) -> bool:
        percent_health = 1 - ((self.max_hp - self.hp) / self.max_hp)
        if self.friendliness == 1:
            return not randint(0, int(50 * percent_health) + 30)
        if self.friendliness == 2:
            return not randint(0, int(20 * percent_health) + 10)
        if self.friendliness == 3:
            return not randint(0, int(10 * percent_health) + 10)
        if self.friendliness == 4:
            return not randint(0, int(10 * percent_health) + 1)
        return not randint(0, 1)


class Hound(Animal):
    def __init__(self, hp: int = 2, atk: int = 2, spd: int = 2, friendliness: int = 4, is_wild: bool = True):
        Animal.__init__(self, hp, atk, spd, friendliness, is_wild=is_wild, name="Hound")


class Cat(Animal):
    def __init__(self, hp: int = 3, atk: int = 1, spd: int = 3, friendliness: int = 3, is_wild: bool = True):
        Animal.__init__(self, hp, atk, spd, friendliness, is_wild=is_wild, name="Cat")


class Squirrel(Animal):
    def __init__(self, hp: int = 1, atk: int = 1, spd: int = 2, friendliness: int = 5, is_wild: bool = True):
        Animal.__init__(self, hp, atk, spd, friendliness, is_wild=is_wild, name="Squirrel")
