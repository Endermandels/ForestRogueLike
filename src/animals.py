from __future__ import annotations
from typing import Optional, Callable
from toolbox import clamp, scroll
from colorama import Fore, Style
from random import randint
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
        self.poisoned: bool = False

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

        if self.poisoned:
            scroll(f"! {self} suffered from poison")
            self.take_dmg(None, 1)

    def execute_action(self):
        # Can't execute action if already dead
        if self.is_dead():
            return

        self.action(self.action_target)
        self.gain_xp(self.xp_per_action)

        # Reset stored action target
        self.action_target = None

    def take_dmg(self, enemy: Animal, amount: int, poison: bool = False):
        # Can't take damage if already dead
        if self.is_dead():
            return

        old_hp = self.hp
        self.hp = clamp(self.hp - amount, 0, self.max_hp)
        scroll(f"! {self} took {Fore.YELLOW}{old_hp - self.hp}{Style.RESET_ALL} damage")

        if poison:
            self.poisoned = True

        if self.is_dead():
            scroll(f"! {self} {Fore.RED}died{Style.RESET_ALL}")

    def is_dead(self) -> bool:
        return self.hp <= 0

    def can_attack(self) -> bool:
        return not self.is_dead()

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
            self.max_hp += 2
            self.hp = self.max_hp
            scroll(f"$ Your {self} increased its {Fore.YELLOW}HP{Style.RESET_ALL}")

    def clear_training_buff(self):
        self.training_buff = Buff.NONE

    def gain_xp(self, xp):
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


class Grizzly(Animal):
    def __init__(
        self, hp: int = 6, atk: int = 4, spd: int = 1, friendliness: int = 1, is_wild: bool = True
    ):
        Animal.__init__(self, hp, atk, spd, friendliness, is_wild=is_wild, name="Grizzly")
        self.action = self._action

    def _action(self, target: Animal):
        if target.can_be_attacked():
            scroll(f"! {self} attacked {target}")
            target.take_dmg(self, self.atk)

    def _become_alpha(self):
        # TODO: Implement
        pass


class Hound(Animal):
    def __init__(
        self, hp: int = 2, atk: int = 2, spd: int = 2, friendliness: int = 4, is_wild: bool = True
    ):
        Animal.__init__(self, hp, atk, spd, friendliness, is_wild=is_wild, name="Hound")
        self.action = self._action

    def _action(self, target: Animal):
        if target.can_be_attacked():
            scroll(f"! {self} attacked {target}")
            target.take_dmg(self, self.atk)

    def _become_alpha(self):
        # TODO: Implement
        pass


class Cat(Animal):
    def __init__(
        self,
        hp: int = 2,
        atk: int = 1,
        spd: int = 3,
        friendliness: int = 3,
        xp_thresh: int = 100,
        xp_per_action: int = 5,
        xp_per_train_hp: int = 10,
        xp_per_train_atk: int = 20,
        is_wild: bool = True,
    ):
        Animal.__init__(
            self,
            hp,
            atk,
            spd,
            friendliness,
            xp_thresh,
            xp_per_action,
            xp_per_train_hp,
            xp_per_train_atk,
            is_wild=is_wild,
            name="Cat",
        )
        self.action = self._action
        self.first_attack: bool = True
        self.first_attack_bonus: int = 1

    def _action(self, target: Animal):
        if target.can_be_attacked():
            scroll(f"! {self} attacked {target}")
            if self.first_attack:
                target.take_dmg(self, self.atk + self.first_attack_bonus)
            else:
                target.take_dmg(self, self.atk)
            self.first_attack = False

    def _alpha_action(self, target: Animal):
        self.invulnerable = self.first_attack
        self._action(target)

    def reset_stats(self):
        super().reset_stats()
        self.first_attack = True

    def _become_alpha(self):
        self.first_attack_bonus = 3
        self.max_hp += 2
        self.hp += 2
        self.atk += 1
        self.action = self._alpha_action
        print(f"$ {self} became an Alpha {self}")


class Squirrel(Animal):
    def __init__(
        self, hp: int = 1, atk: int = 1, spd: int = 2, friendliness: int = 5, is_wild: bool = True
    ):
        Animal.__init__(self, hp, atk, spd, friendliness, is_wild=is_wild, name="Squirrel")
        self.action = self._action

    def _action(self, target: Animal):
        if target.can_be_attacked():
            scroll(f"! {self} attacked {target}")
            target.take_dmg(self, self.atk)

    def _become_alpha(self):
        # TODO: Implement
        pass


class Snake(Animal):
    def __init__(
        self, hp: int = 1, atk: int = 1, spd: int = 2, friendliness: int = 3, is_wild: bool = True
    ):
        Animal.__init__(self, hp, atk, spd, friendliness, is_wild=is_wild, name="Snake")
        self.action = self._action

    def _action(self, target: Animal):
        if target.can_be_attacked():
            scroll(f"! {self} attacked and poisoned {target}")
            target.take_dmg(self, self.atk, poison=True)

    def _become_alpha(self):
        # TODO: Implement
        pass
