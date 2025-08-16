from animals import *
from random import choice
from toolbox import *


class AIHandler:
    """
    Acts as an opponent would act IRL
    """

    def __init__(self):
        self.party: list[Animal] = []

    def randomize_party(self):
        ENCOUNTERS = [
            [Squirrel(), Squirrel(), Squirrel()],
            [Squirrel(), Squirrel()],
            [Squirrel(), Squirrel()],
            [Squirrel()],
            [Hound(), Squirrel()],
            [Hound()],
            [Hound()],
            [Cat()],
        ]
        self.party = choice(ENCOUNTERS)

    def boss_party(self):
        self.party = [Grizzly(), Hound()]  # TODO: Fix this

    def decide_targets(self, my_animals: list[Animal], enemy_animals: list[Animal]):
        """
        Decide which animals attack which opponents
        """
        for my_animal in my_animals:
            my_animal.set_target(choice(enemy_animals))

    def remove_dead_animals(self):
        remove_dead_animals(self.party)

    def remove_animal(self, animal: Animal):
        self.party.remove(animal)

    def all_animals_dead(self) -> bool:
        return len(self.party) < 1

    def animals_that_can_attack(self) -> list[Animal]:
        return filter_can_attack(self.party)

    def animals_that_can_be_attacked(self) -> list[Animal]:
        return filter_can_be_attacked(self.party)

    def get_willing_animals(self) -> list[Animal]:
        return [animal for animal in self.party if animal.is_willing_to_join_player()]
