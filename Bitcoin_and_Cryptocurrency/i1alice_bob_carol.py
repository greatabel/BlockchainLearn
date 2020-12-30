from threading import Thread

from time import sleep
from termcolor import colored

# import random
from random import randint

medicinePrice = 10
toolPrice = 20
foodPrice = 5


class TradingPeople(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        mesage = "I'm " + name
        if name == "alice":
            mesage += " I have medicines, I need tools. \n"
            self.medicineNum = 10
            self.toolNum = 0
            self.foodNum = 0
        elif name == "bob":
            mesage += " I have tools, I need medicines. \n"
            self.medicineNum = 0
            self.toolNum = 5
            self.foodNum = 0
        elif name == "carol":
            mesage += " I have tools, I need medicines. \n"
            self.medicineNum = 0
            self.toolNum = 0
            self.foodNum = 20
        self.message = mesage

    def print_message(self):
        print(self.message)

    def offer_trade(self):
        # if hasattr(self, 'medicineNum'):
        print(self.name, "'s medicineNum:", self.medicineNum)
        print(self.name, "'s toolNum:", self.toolNum)
        print(self.name, "'s foodNum:", self.foodNum)
        print("\n")

    def trading(self):
        if (
            hasattr(self, "medicineNum")
            and hasattr(self, "toolNum")
            and hasattr(self, "foodNum")
        ):
            # if random.choice([True, False]):
            if randint(0, 5) == 0:
                self.medicineNum -= 2
                self.toolNum += 1
            elif randint(0, 5) == 1:
                self.medicineNum += 2
                self.toolNum -= 1
            elif randint(0, 5) == 2:
                self.medicineNum += 1
                self.foodNum -= 2
            elif randint(0, 5) == 3:
                self.toolNum += 1
                self.foodNum -= 4
            elif randint(0, 5) == 4:
                self.medicineNum -= 1
                self.foodNum += 2
            elif randint(0, 5) == 5:
                self.toolNum -= 1
                self.foodNum += 4

    def run(self):
        print("Trading thread starting\n")
        x = 0
        while x < 10:
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
    carol = TradingPeople("carol")
    carol.start()
    print(colored("Main Process end", "blue"), "*" * 10)


if __name__ == "__main__":
    main()
