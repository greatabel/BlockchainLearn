import threading
import time
import datetime
import random
import operator
from termcolor import colored

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