from animals import Animal

class Player:
    def __init__(self):
        self.party: list[Animal] = []
    
    def add_animal(self, animal: Animal):
        animal.tame()
        self.party.append(animal)
        print(f'{animal} joined your party')