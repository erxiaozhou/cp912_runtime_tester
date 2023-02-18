import random

def delete_random_character(s:bytearray):
    """Returns s with a random character deleted"""
    if len(s) == 0:
        return s
    s = s.copy()
    pos = random.randint(0, len(s) - 1)
    s.pop(pos)
    return s

def insert_random_character(s):
    """Returns s with a random character inserted"""
    s = s.copy()
    pos = random.randint(0, len(s))
    random_character = random.randint(0,255)
    s.insert(pos, random_character)
    return s

def flip_random_character(s):
    """Returns s with a random bit flipped in a random position"""
    if len(s) == 0:
        return s
    s = s.copy()
    pos = random.randint(0, len(s) - 1)
    bit = 1 << random.randint(0, 7)
    s[pos] = s[pos] ^ bit
    return s

def replace_random_character(s):
    if len(s) == 0:
        return s
    s = s.copy()
    pos = random.randint(0, len(s) - 1)
    s[pos] = random.randint(0,255)
    return s


def mutate(s):
    """Return s with a random mutation applied"""
    mutators = [
        delete_random_character,
        insert_random_character,
        # flip_random_character,
        replace_random_character
    ]
    mutator = random.choice(mutators)
    return mutator(s)
