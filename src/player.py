from animals import Animal

class Player:
    def __init__(self):
        self.party = []
    
    def add_animal(self, animal: Animal):
        self.party.append(animal)
        print(f'A wild {animal.name} joined your party')