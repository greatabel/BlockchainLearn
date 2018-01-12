from threading import Thread

from time import sleep
from termcolor import colored
import random

medicinePrice = 10
toolPrice = 20

class TradingPeople(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        mesage = "I'm " + name
        if name  == "alice":
            mesage += " I have medicines, I need tools. \n"
            self.medicineNum = 10
            self.toolNum = 0

        elif name == "bob":
            mesage += " I have tools, I need medicines. \n" 
            self.medicineNum = 0
            self.toolNum = 5    

        self.message = mesage

    def print_message(self):
        print(self.message)

    def offer_trade(self):
        # if hasattr(self, 'medicineNum'):
        print(self.name ,"'s medicineNum:", self.medicineNum)
        # elif hasattr(self, 'toolNum'):
        print(self.name, "'s toolNum:", self.toolNum)

    def trading(self):
        if hasattr(self, 'medicineNum') and hasattr(self, 'toolNum'):
            if random.choice([True, False]):
                self.medicineNum  -= 2
                self.toolNum += 1
            else:
                self.medicineNum  += 2
                self.toolNum -= 1               


    def run(self):
        print("Trading thread starting\n")
        x = 0 
        while( x < 10):
            self.print_message()
            self.offer_trade()
            self.trading()
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
