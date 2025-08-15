from animals import Animal
from toolbox import *
import sys


class Player:
    def __init__(self):
        self.party: list[Animal] = []

    def add_animal(self, animal: Animal):
        animal.tame()
        self.party.append(animal)
        print(f"$ {animal} joined your party")

    def train_animal(self, idx: int):
        if idx < 0 or idx >= len(self.party):
            print(f"### Incorrect idx: {idx} ###")
            sys.exit()

        self.party[idx].train()

        for animal in self.party:
            animal.clear_training_buff()

    def reset_animal_stats(self):
        for animal in self.party:
            animal.reset_stats()

    def decide_training_buffs(self):
        for animal in self.party:
            animal.decide_training_buff()

    def remove_dead_animals(self):
        remove_dead_animals(self.party)

    def all_animals_dead(self) -> bool:
        return len(self.party) < 1

    def animals_that_can_attack(self) -> list[Animal]:
        return filter_can_attack(self.party)

    def animals_that_can_be_attacked(self) -> list[Animal]:
        return filter_can_be_attacked(self.party)
