from threading import Thread

from time import sleep


class TradingPeople(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.message = "I'm " + name

    def print_message(self):
        print(self.message)

    def run(self):
        print("Thread starting\n")
        x = 0 
        while( x < 10):
            self.print_message()
            sleep(1)
            x += 1
        print("Thread Ended\n")

print("Main Process start")

alice = TradingPeople("alice")
alice.start()
bob = TradingPeople("bob")
bob.start()

print("Main Process end.")