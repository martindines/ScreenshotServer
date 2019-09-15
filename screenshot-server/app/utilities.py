from random import sample
from string import digits, ascii_letters


def get_random_hash(length=8):
    return "".join(sample(digits + ascii_letters, length))
