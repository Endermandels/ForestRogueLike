def clamp(val, minimum, maximum):
    if val < minimum:
        return minimum
    return maximum if val > maximum else val


def all_animals_dead(animals: list) -> bool:
    """
    Returns whether all animals in the given list are dead.
    """
    for animal in animals:
        if not animal.is_dead():
            return False
    return True


def remove_dead_animals(animals: list):
    """
    Remove (in place) all dead animals from given list of animals.
    """
    to_remove = []
    for animal in animals:
        if animal.is_dead():
            to_remove.append(animal)
    for animal in to_remove:
        animals.remove(animal)


def filter_can_attack(animals: list) -> list:
    return list(filter(lambda x: x.can_attack(), animals))


def filter_can_be_attacked(animals: list) -> list:
    return list(filter(lambda x: x.can_be_attacked(), animals))
