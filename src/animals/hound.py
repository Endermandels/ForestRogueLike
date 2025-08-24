from .animal import Animal
from toolbox import scroll


class Hound(Animal):
    def __init__(
        self,
        hp: int = 2,
        atk: int = 2,
        spd: int = 2,
        friendliness: int = 4,
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
            name="Hound",
        )
        self.action = self._action

    def _action(self, target: Animal):
        if target and target.can_be_attacked():
            scroll(f"! {self} attacked {target}")
            target.take_dmg(self, self.atk)

    def _become_alpha(self):
        # TODO: Implement
        pass
