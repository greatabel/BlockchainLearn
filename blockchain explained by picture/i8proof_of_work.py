import string
import random
import time

import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt
from termcolor import colored


timelist = []


def show(s, color='green'):
    print(colored(s, color, attrs=['reverse', 'blink']))


def id_generator(size=6):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))


def turn():
    global time_count_dic
    start = time.time()
    try_count = 0
    while True:
        block_prefix = id_generator()
        try_count += 1
        if block_prefix.startswith("000"):
            end = time.time()
            span = round(end - start, 2)
            print(block_prefix + ' time= ' + str(span) + ' ' + str(try_count))
            timelist.append(span)
            break


def draw_chart():
    timelist.sort()
    time_mean = np.mean(timelist)
    time_std = np.std(timelist)
    pdf = stats.norm.pdf(timelist, time_mean, time_std)
    plt.plot(timelist, pdf)
    plt.show()


def main():
    for i in range(10**2):
        turn()
    show(timelist)
    show('POW 时间分布图:', color='red')
    draw_chart()


if __name__ == "__main__":
    main()
