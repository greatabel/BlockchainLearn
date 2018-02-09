from threading import Thread, Event
import threading
from queue import Queue
import time
import random
from termcolor import colored

# 实用拜占庭容错算法PBFT
# https://www.jianshu.com/p/1e2acd3cbd9f

def show(s,color='green'):
    return colored(s, color, attrs=['reverse', 'blink'])

def PBFT(results):
    print(results)
    # PBFT算法的核心理论是n>=3f+1
    max_key = max(results, key=results.get)
    max_value = results[max_key]
    n = sum(results.values())
    if max_value >= (n - 1) * 2 / 3:
        print("PBFT 决定接受方案:", max_key)
    else:
        print("PBFT 无法满足做出决策条件")

class Starter(Thread):
    def __init__(self, queue, r_queue):
        Thread.__init__(self)
        self.queue = queue
        self.response_queue = r_queue

    def run(self):
        for i in range(10):
            item = 'move #east# 500km'
            self.queue.put(item)
            print ('Starter notify : item %s appended to queue by %s \n'\
                    % (item, self.name))
            time.sleep(0.2)
        results = {}
        while True:
            r_item = self.response_queue.get()
            if self.response_queue.qsize() == 0:
                break
            print('r_item:', r_item, self.response_queue.qsize())
            if r_item in results:
                results[r_item] += 1
            else:
                results[r_item] = 1
            self.response_queue.task_done()

        PBFT(results)



class CmdExecutor(Thread):
    def __init__(self, queue, r_queue):
        Thread.__init__(self)
        self.queue = queue
        self.response_queue = r_queue

    def run(self):
        while True:
            item = self.queue.get()
            tid = int(threading.currentThread().getName()[-1])
            myrandom = random.randint(1, 5)
            if tid % myrandom == 0:
                item = item.replace("#east#", "#west#")
                showitem = show(item)
                print ('CmdExecutor execute :', showitem )
            else:
                print ('CmdExecutor execute :', item )
            self.queue.task_done()
            response_item = item.replace("move", "moved")

            self.response_queue.put(response_item)


if __name__ == '__main__':
        queue = Queue()
        r_queue = Queue()
        t1 = Starter(queue, r_queue)
        t1.start()
        CmdExecutorList = []
        for i in range(5):
            t = CmdExecutor(queue, r_queue)
            CmdExecutorList.append(t)

        for t in CmdExecutorList:
            t.start()

        t1.join()
        for t in CmdExecutorList:
            t.join()
        print('Main exit.')