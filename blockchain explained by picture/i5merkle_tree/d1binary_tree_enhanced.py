import string
import random

characters = string.ascii_uppercase + string.digits + string.ascii_lowercase 
digits = string.digits

def id_generator(size=6, chars=characters ):
    return ''.join(random.choice(chars) for _ in range(size))

class Block:
    def __init__(self):
        self.id =  id_generator(size=3, chars=digits)
        self.data = id_generator(size=20, chars=characters)
        self.digest = self.data[0:5]

class Node:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val


class Tree:
    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def add_node(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if(val < node.val):
            if node.left is not None:
                self._add(val, node.left)
            else:
                node.left = Node(val)
        else:
            if node.right is not None:
                self._add(val, node.right)
            else:
                node.right = Node(val)

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)

    def _print_tree(self, node):
        if node is not None:            
            self._print_tree(node.left)
            print(str(node.val), end='')          
            self._print_tree(node.right)
        else:
            print("\t")


def main():
    tree = Tree()
    tree.add_node(5)
    tree.add_node(10)
    tree.add_node(0)
    tree.add_node(16)
    tree.add_node(2)
    tree.print_tree()
    block = Block()
    print(block.id, block.data, block.digest)



if __name__ == "__main__":
    main()
