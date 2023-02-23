import random


def in_masks(pos, masks):
    is_in_mask = False
    for m in masks:
        if pos >= m[0] and pos < m[1]:
            is_in_mask = True
    return is_in_mask


def get_pos_outof_masks(s, masks):
    while True:
        pos = random.randint(0, len(s) - 1)
        if not in_masks(pos, masks):
            break
    return pos


def get_pos_outof_masks_insert(s, masks):
    ms2 = [[m[0] + 1, m[1]] for m in masks]
    while True:
        pos = random.randint(0, len(s))
        if not in_masks(pos, ms2):
            break
    return pos


def _delete_random_character(s: bytearray, masks):
    """Returns s with a random character deleted"""
    if len(s) == 0:
        return s
    s = s.copy()
    pos = get_pos_outof_masks(s, masks)
    # print('delete pos', pos, masks)
    s.pop(pos)
    return s


def _insert_random_character(s, masks):
    """Returns s with a random character inserted"""
    s = s.copy()
    pos = get_pos_outof_masks_insert(s, masks)
    # print('insert pos', pos, masks)
    random_character = random.randint(0, 255)
    s.insert(pos, random_character)
    return s


# def flip_random_character(s, masks):
#     """Returns s with a random bit flipped in a random position"""
#     if len(s) == 0:
#         return s
#     s = s.copy()
#     pos = get_pos_outof_masks(s, masks)
#     bit = 1 << random.randint(0, 7)
#     s[pos] = s[pos] ^ bit
#     return s


def _replace_random_character(s, masks):
    if len(s) == 0:
        return s
    s = s.copy()
    pos = get_pos_outof_masks(s, masks)
    # print('replace pos', pos, masks)
    s[pos] = random.randint(0, 255)
    return s


def mutate_with_mask(s, masks):
    """Return s with a random mutation applied"""
    mutators = [
        _delete_random_character,
        _insert_random_character,
        # flip_random_character,
        _replace_random_character
    ]
    mutator = random.choice(mutators)
    return mutator(s, masks)
