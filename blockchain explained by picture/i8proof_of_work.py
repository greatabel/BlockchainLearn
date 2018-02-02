import string
import random
import time
from termcolor import colored

def show(s,color='green'):
    print(colored(s, color, attrs=['reverse', 'blink']))

def id_generator(size=6):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase 
    return ''.join(random.choice(chars) for _ in range(size))


def main():
    try_count = 0
    while True:
        block_prefix = id_generator()
        try_count += 1
        
        if block_prefix.startswith("000"):
            show(block_prefix)
            break

        print(block_prefix, try_count)

if __name__ == "__main__":
    main()