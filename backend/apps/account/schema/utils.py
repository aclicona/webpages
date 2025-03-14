import string
import random


def random_string():
    return ''.join(random.choice(string.ascii_letters) for _i in range(6)) + ''.join(
        random.choice(string.punctuation) for _i in range(4)) + ''.join(
        random.choice(string.digits) for _i in range(2))
