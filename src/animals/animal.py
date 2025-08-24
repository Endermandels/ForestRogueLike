from __future__ import annotations
from typing import Optional, Callable
from toolbox import clamp, scroll
from colorama import Fore, Style
from random import randint
from enum import Enum


# Training Buffs
class Buff(Enum):
    ATK = "ATK"
    HP = "HP"
    NONE = ""


class Animal:
    def __init__(
        self,
        hp: int,
        atk: int,
        spd: int,
        friendliness: int,
        xp_thresh: int,
        xp_per_action: int,
        xp_per_train_hp: int,
        xp_per_train_atk: int,
        is_wild: bool = True,
        name: str = "Animal",
    ):
        """
        Stats breakdown:
            HP (health points): 1-6
            ATK (attack): 1-4
            SPD (speed): 1-3
            FRE (friendliness): 1-5

        Effects breakdown:
            Poison - Deal X damage per turn
            Paralysis - Wait X turns until immobilized, meaning that this Animal cannot perform any actions.  X is never less than 1
            Invulnerable - This Animal cannot take any damage this turn
        """
        # ID
        self.name: str = name
        self.is_wild: bool = is_wild

        # Stats
        self.max_hp: int = hp
        self.hp: int = self.max_hp
        self.atk: int = atk
        self.spd: int = spd

        # Hidden stats
        self.friendliness: int = friendliness
        self.xp: int = 0
        self.xp_thresh: int = xp_thresh
        self.xp_per_action: int = xp_per_action
        self.xp_per_train_hp: int = xp_per_train_hp
        self.xp_per_train_atk: int = xp_per_train_atk

        # Intentions
        self.action: Optional[Callable[[Animal], None]] = None
        self.action_target: Animal = None
        self.training_buff: Buff = Buff.NONE

        # Effects
        self.invulnerable: bool = False
        self.poisoned: int = -1  # Damage per turn (-1 for no poison)
        self.paralyzed: int = -1  # Number of turns before paralysis (-1 for no paralysis)

    def __repr__(self) -> str:
        return (
            # f"{Fore.RED + 'Wild' if self.is_wild else Fore.GREEN + 'Tamed'}"
            f"{Fore.RED if self.is_wild else Fore.GREEN}"
            f"{self.name}{Style.RESET_ALL}"
            f" ({self.hp}{Fore.YELLOW + ' +2' + Style.RESET_ALL if self.training_buff == Buff.HP else ''}):"
            f" [{self.atk}{Fore.YELLOW + ' +1' + Style.RESET_ALL if self.training_buff == Buff.ATK else ''}]"
            f" [{self.spd}]"
        )

    def set_target(self, target: Animal):
        self.action_target = target

    def apply_after_effects(self):
        """
        Apply effects after all actions have been resolved.
        """
        # Can't apply effects if already dead
        if self.is_dead():
            return

        if self.poisoned > 0:
            scroll(f"! {self} suffered from poison")
            self.take_dmg(None, self.poisoned)

        if self.paralyzed > 0:
            self.paralyzed -= 1
            if self.paralyzed == 0:
                scroll(f"! {self} fell to the ground paralyzed")

    def execute_action(self):
        # Can't execute action if already dead
        if self.can_attack():
            return

        self.action(self.action_target)
        self.gain_xp(self.xp_per_action)

        # Reset stored action target
        self.action_target = None

    def take_dmg(self, enemy: Animal, amount: int):
        # Can't take damage if already dead
        if self.is_dead():
            return

        old_hp = self.hp
        self.hp = clamp(self.hp - amount, 0, self.max_hp)
        scroll(f"! {self} took {Fore.YELLOW}{old_hp - self.hp}{Style.RESET_ALL} damage")

        if self.is_dead():
            scroll(f"! {self} {Fore.RED}died{Style.RESET_ALL}")

    def paralyze(self, nturns: int):
        """nturns should be no less than 1"""
        if self.paralyzed < 0 and nturns > 0:
            self.paralyzed = nturns

    def poison(self, amount: int):
        if amount > self.poisoned:
            self.poisoned = amount

    def is_dead(self) -> bool:
        return self.hp <= 0

    def can_attack(self) -> bool:
        return not self.is_dead() and self.paralyzed != 0

    def can_be_attacked(self) -> bool:
        return not self.is_dead() and not self.invulnerable

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
            self.atk += 1
            scroll(f"$ Your {self} increased its {Fore.YELLOW}ATK{Style.RESET_ALL}")
        if self.training_buff == Buff.HP:
            self.training_buff = Buff.NONE
            self._increase_base_hp(2)
            scroll(f"$ Your {self} increased its {Fore.YELLOW}HP{Style.RESET_ALL}")

    def clear_training_buff(self):
        self.training_buff = Buff.NONE

    def gain_xp(self, xp: int):
        # Can't gain XP if already maxxed out
        if self.xp >= self.xp_thresh:
            return

        scroll(f"* {self} gained {Fore.YELLOW}{xp}{Style.RESET_ALL} XP")
        self.xp += xp
        if self.xp >= self.xp_thresh:
            self._become_alpha()

    def _become_alpha(self):
        # TODO: Implement
        pass

    def reset_stats(self):
        self.hp = self.max_hp
        self.poisoned = -1
        self.paralyzed = -1

    def is_willing_to_join_player(self) -> bool:
        percent_health = 1 - ((self.max_hp - self.hp) / self.max_hp)
        if self.friendliness == 0:
            return False
        if self.friendliness == 1:
            return not randint(0, int(50 * percent_health) + 30)
        if self.friendliness == 2:
            return not randint(0, int(20 * percent_health) + 10)
        if self.friendliness == 3:
            return not randint(0, int(10 * percent_health) + 10)
        if self.friendliness == 4:
            return not randint(0, int(10 * percent_health) + 1)
        return not randint(0, 1)

    def _increase_base_hp(self, amount: int):
        self.max_hp += amount
        self.hp += amount
