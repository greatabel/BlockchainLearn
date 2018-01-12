from threading import Thread

from time import sleep
from termcolor import colored


medicinePrice = 10
toolPrice = 20

class TradingPeople(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        mesage = "I'm " + name
        if name  == "alice":
            mesage += " I have medicines, I need tools. \n"
            self.medicineNum = 10

        elif name == "bob":
            mesage += " I have tools, I need medicines. \n" 
            self.toolNum = 5           
        self.message = mesage

    def print_message(self):
        print(self.message)

    def offer_trade(self):
        if hasattr(self, 'medicineNum'):
            print("medicineNum:", self.medicineNum)
        elif hasattr(self, 'toolNum'):
            print("toolNum:", self.toolNum)

    def run(self):
        print("Trading thread starting\n")
        x = 0 
        while( x < 10):
            self.print_message()
            self.offer_trade()
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
