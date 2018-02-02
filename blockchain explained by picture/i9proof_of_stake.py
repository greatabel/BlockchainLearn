import string
import random
import time

import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt
from termcolor import colored


timelist = []
stake_timelist = []

def show(s, color='green'):
    print(colored(s, color, attrs=['reverse', 'blink']))


def id_generator(size=6):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))


def turn(with_stake=False):
    global time_count_dic
    start = time.time()
    try_count = 0
    while True:
        block_prefix = id_generator()
        # 为简化，我们假设PoS代币数目都是相同的等级
        if with_stake:
            block_prefix = '0' + block_prefix[1:]
        try_count += 1
        if block_prefix.startswith("000"):
            end = time.time()
            span = round(end - start, 2)
            print(block_prefix + ' time= ' + str(span) + ' ' + str(try_count),
                    'with_stake:', with_stake)
            if with_stake:
                stake_timelist.append(span)
            else:
                timelist.append(span)
            break


def draw_chart(tl):
    tl.sort()
    time_mean = np.mean(tl)
    time_std = np.std(tl)
    pdf = stats.norm.pdf(tl, time_mean, time_std)
    plt.plot(tl, pdf)
    # plt.show()


def main():
    for i in range(50):
        turn()
        turn(True)
    show(timelist)
    show(stake_timelist, color='cyan')
    show('[PoW VS PoS] 时间分布图:', color='red')
    draw_chart(timelist)
    draw_chart(stake_timelist)
    plt.show()

if __name__ == "__main__":
    main()
