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

# 暂时模拟第1个要求大概，有空模拟其他的

age_of_this_universe = 1024  # unit:seconds

semaphore = threading.Semaphore(0)
threshold = 0.5

def show(s,color='green'):
    print(colored(s, color, attrs=['reverse', 'blink']), now_time())

def now_time():
    return datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")


listings = {}
notebook = []
def consumer():
    myname = threading.currentThread().getName()
    print(myname + " consumer is waiting")
    while threading.activeCount() > 2:
        semaphore.acquire()
        # print('consumer lock it, when threading.activeCount()= ' + str(threading.activeCount())
        #         + ' len(listings)=' + str(len(listings)))
        if len(listings) > threshold * threading.activeCount():
            using_one = max(listings, key=listings.get)
            if listings[using_one] not in notebook:
                print("among the %s" %listings)
                show("Consumer notify : consumed item number %s" %using_one)
                notebook.append(listings[using_one])
                show(notebook, "cyan")
        print('consumer threading.activeCount()=', threading.activeCount())
        if threading.activeCount() <= 2:
            break
    print('consumer is gone!')

def mining():
    time.sleep(random.random() * 10)
    item = random.randint(0, 100)
    return item

def producer():
    global listings
    item = mining()
    myname = threading.currentThread().getName()
    listings[myname] =  item
    print ("producer " + myname + " notify : producted item number %s" %item)
    semaphore.release()

    time.sleep(random.random() * 10)
    del listings[myname]
    print ("producer " + myname + " is gone.")

def main():
    start = time.time()
    block_scheduler = threading.Thread(target=consumer)
    block_scheduler.start()
    global minerThreads 
    minerThreads = []
    while True:        
        minerNum = random.randint(0, 50)
        for i in range(1, minerNum):
            minerThreads.append(threading.Thread(target=producer))

        for miner in minerThreads:
            miner.start()
        
        for miner in minerThreads:
            miner.join()        

        minerThreads = []
        show('- >'*20, 'magenta')
        end = time.time()
        show('time= %s' %(end - start))
        if (end - start) >= age_of_this_universe:
            print('Bang!')
            semaphore.release()
            break

    block_scheduler.join()

if __name__ == '__main__':
    print (threading.currentThread().getName() + " main program started")
    main()
    print (threading.currentThread().getName() + " main program terminated")
