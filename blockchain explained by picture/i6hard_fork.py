import string
import random
import functools


def id_generator(size=6):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase 
    return ''.join(random.choice(chars) for _ in range(size))

class Block:
    def __init__(self):
        self.id =  random.randint(0, 100)
        self.data = id_generator(size=20)
        self.digest = self.data[0:5]

class NewBlock:
    def __init__(self):
        self.id =  random.randint(0, 100)
        self.data = id_generator(size=40)
        self.digest = self.data[0:10]