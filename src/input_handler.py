from animals import Animal

class InputHandler:
    def __init__(self):
        pass
    
    def decide_targets(self, my_animals: list[Animal], enemy_animals: list[Animal]):
        for my_animal in my_animals:
            print(f'* Choose which animal your {my_animal} attacks')
            idx = self.get_choice(enemy_animals)
            my_animal.set_target(enemy_animals[idx])
    
    def get_choice(self, options: list) -> int:
        '''
        Given a list of options to choose from, return the index of the selected choice.
        '''
        idx = -1
        input_str = '* Choose from the following options:\n'
        
        for i, option in enumerate(options):
            input_str += f'  {i+1}. {option}\n'
            
        while idx < 0:
            inp = input(input_str + ">> ").strip()
            if not inp.isnumeric():
                print("! Please input one of the option numbers")
                continue
            inp = int(inp)
            if inp < 1 or inp > len(options):
                print("! Please input one of the option numbers")
                continue
            idx = inp - 1
            
        return idx