from .animal import Animal
from toolbox import scroll


class Cat(Animal):
    def __init__(
        self,
        hp: int = 2,
        atk: int = 1,
        spd: int = 3,
        friendliness: int = 3,
        xp_thresh: int = 20,
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
        if target and target.can_be_attacked():
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
        self._increase_base_hp(3)
        self.atk += 1
        self.action = self._alpha_action
        scroll(f"$ {self} became an Alpha {self}")
