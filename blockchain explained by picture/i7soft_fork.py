import string
import random
# import functools


def id_generator(size=6):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))


class Block:
    def __init__(self):
        self.id = random.randint(0, 100)
        self.data = id_generator(size=20)
        self.digest = self.data[0:5]

    def __str__(self):
            return str(self.id)


class NewBlock:
    def __init__(self):
        self.id = random.randint(0, 100)
        self.data = id_generator(size=40)
        self.digest = self.data[0:10]

    def __str__(self):
        return str(self.id)

class Node:
    def __init__(self):
        self.data = None
        self.next = None


class LinkedList:
    def __init__(self):
        self.current_node = None

    def add_node(self, data):
        if not isinstance(data, Block) and  not isinstance(data, NewBlock):
            print(data, "属于", type(data), "我们不是一个组织系统的，你去别地方挖煤吧！")
            return 
        elif isinstance(data, NewBlock):
            print(data, "属于我们接受的软分叉，过来一起挖吧！")
        new_node = Node()
        new_node.data = data
        new_node.next = self.current_node
        self.current_node = new_node

    def show(self):
        node = self.current_node
        while node:
            print(node.data)
            node = node.next


if __name__ == "__main__":
    mylist = LinkedList()
    for i in range(0, 10):
        mylist.add_node(Block())
    for i in range(0, 5):
        mylist.add_node(NewBlock())
    print('#' * 20)
    mylist.show()
