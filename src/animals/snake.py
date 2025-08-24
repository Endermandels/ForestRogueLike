from .animal import Animal
from toolbox import scroll


class Snake(Animal):
    def __init__(
        self,
        hp: int = 1,
        atk: int = 1,
        spd: int = 2,
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
            name="Snake",
        )
        self.action = self._action

    def _action(self, target: Animal):
        if target and target.can_be_attacked():
            scroll(f"! {self} attacked and poisoned {target}")
            target.take_dmg(self, self.atk)
            target.poison(1)

    def _alpha_action(self, target: Animal):
        if target and target.can_be_attacked():
            scroll(f"! {self} attacked and poisoned {target}")
            target.take_dmg(self, self.atk)
            target.poison(2)
            target.paralyze(3)

    def _become_alpha(self):
        self._increase_base_hp(1)
        self.atk += 1
        self.action = self._alpha_action
        scroll(f"$ {self} became an Alpha {self}")
