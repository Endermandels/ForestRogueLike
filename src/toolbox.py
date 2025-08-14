def clamp(val, minimum, maximum):
    if val < minimum:
        return minimum
    return maximum if val > maximum else val

def all_animals_dead(animals: list):
    for animal in animals:
        if not animal.is_dead():
            return False
    return True