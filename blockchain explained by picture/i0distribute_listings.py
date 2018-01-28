import threading
import time
import datetime
import random
import operator
from termcolor import colored

# 1. 可以无限增加的巨型账本——每个区块可以视作这个账本的一页，
#    每增加一个区块，账本就多了一页，这一页中可能会包含一条或多条记录信息；
# 2. 加密且有顺序的账本——账目信息会被打包成一个区块并加密，同时盖上时间戳，
#    一个个区块按时间戳顺序链接形成一个总账本；
# 3. 去中心化的账本——由网内用户共同维护的，它是去中心化的。


def show(s,color='green'):
    print(colored(s, color, attrs=['reverse', 'blink']), now_time())

def now_time():
    return datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

semaphore = threading.Semaphore(0)
threshold = 5

listings = {}
notebook = []
def consumer():
    print("consumer is waiting")
    while True:
        semaphore.acquire()
        if len(listings) > threshold:
            using_one = max(listings, key=listings.get)
            if listings[using_one] not in notebook:
                print("among the %s" %listings)
                show("Consumer notify : consumed item number %s" %using_one)
                notebook.append(listings[using_one])
                show(notebook, "cyan")

def producer():
    while True:
        global listings
        time.sleep(1.5)
        item = random.randint(0, 100)
        myname = threading.currentThread().getName()
        listings[myname] =  item
        print ("producer " + myname + " notify : producted item number %s" %item)
        semaphore.release()

if __name__ == '__main__':
    minerThreads = []
    for i in range(1, 11):
        minerThreads.append(threading.Thread(target=producer))

    block_scheduler = threading.Thread(target=consumer)
    block_scheduler.start()
    for miner in minerThreads:
        miner.start()

    
    for miner in minerThreads:
        miner.join()
    block_scheduler.join()

    print ("main program terminated")