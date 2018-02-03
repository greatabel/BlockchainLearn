from threading import Thread, Event
import threading
from queue import Queue
import time
import random
from termcolor import colored

def show(s,color='green'):
    return colored(s, color, attrs=['reverse', 'blink'])

class Starter(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        for i in range(20):
            item = 'move #east# 500km'
            self.queue.put(item)
            print ('Starter notify : item %s appended to queue by %s \n'\
                    % (item, self.name))
            time.sleep(0.2)


class CmdExecutor(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            item = self.queue.get()
            tid = int(threading.currentThread().getName()[-1])
            myrandom = random.randint(1, 5)
            if tid % myrandom == 0:
                item = show(item.replace("#east#", "#west#"))
            print ('CmdExecutor execute :', item )

            self.queue.task_done()


if __name__ == '__main__':
        queue = Queue()
        t1 = Starter(queue)
        t1.start()
        CmdExecutorList = []
        for i in range(5):
            t = CmdExecutor(queue)
            CmdExecutorList.append(t)

        for t in CmdExecutorList:
            t.start()

        t1.join()
        for t in CmdExecutorList:
            t.join()
        print('Main exit.')