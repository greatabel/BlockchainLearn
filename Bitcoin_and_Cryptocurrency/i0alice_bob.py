from threading import Thread

from time import sleep
from termcolor import colored


class TradingPeople(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.message = "I'm " + name

    def print_message(self):
        print(self.message)

    def run(self):
        print("Trading thread starting\n")
        x = 0 
        while( x < 10):
            self.print_message()
            sleep(1)
            x += 1
        print("Trading thread Ended\n")

def main():
    print(colored("Main Process start", "red"), "#" * 10)

    alice = TradingPeople("alice")
    alice.start()
    bob = TradingPeople("bob")
    bob.start()

    print(colored("Main Process end", "blue"), "*" * 10)

if __name__ == "__main__":
    main()
