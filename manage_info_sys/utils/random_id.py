import random

num_list = [char for char in '123456789012345678901234567890123456789012340123456789001234567890'\
                             '56789012345678901234567890123456789012345678901234567890']


def generate(id_len=6):
    return random.sample(num_list, id_len)


def generate_account(l, split=''):
    return split.join(generate(l))


