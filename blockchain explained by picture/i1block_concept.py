
# 区块头包含三组元数据：
# 1. 用于连接前面的区块、索引自父区块哈希值的数据；
# 2. 挖矿难度、Nonce（随机数，用于工作量证明算法的计数器）、时间戳；
# 3. 能够总结并快速归纳校验区块中所有交易数据的Merkle（默克尔）树根数据。

# 暂时只实现模拟链结构


class ListNode:
    def __init__(self, data):
        "constructor to initiate this object"

        # store data
        self.data = data        
        # store reference (next item)
        self.next = None
        return
    
    def getData(self):
        return self.data
    
    def setData(self, value):
        self.data = value
        return
    
    def getNext(self):
        return self.next

    def hasValue(self, value):
        if self.data == value:
            return True
        else:
            return False


class SingleLinkedList:
    def __init__(self):
        "constructor to initiate this object"

        self.head = None
        self.tail = None
        return

    def listLength(self):
        "returns the number of list items"        
        count = 0
        currentNode = self.head

        while currentNode is not None:
            # increase counter by one
            count = count + 1
            
            # jump to the linked node
            currentNode = currentNode.getNext()
        
        return count

    def outputList(self):
        "outputs the list (the value of the node, actually)"
        currentNode = self.head

        while currentNode is not None:
            print (currentNode.getData())

            # jump to the linked node
            currentNode = currentNode.getNext()
        
        return

    def addListitem(self, item):
        "add an item at the end of the list"

        if isinstance(item, ListNode):
            if self.head is None:
                self.head = item
            else:
                self.tail.next = item
            self.tail = item
        
        return

    def removeListitemById(self, itemId):
        "remove the list item with the item id"
        
        currentId = 1
        currentNode = self.head
        previousNode = None

        while currentNode is not None:
            if currentId == itemId:
                # if this is the first node (head)
                if previousNode is not None:
                    previousNode.next = currentNode.next
                else:
                    self.head = currentNode.next
                # we don't have to look any further
                return
 
            # needed for the next iteration
            previousNode = currentNode
            currentNode = currentNode.next
            currentId = currentId + 1
                
        return

    def removeListitemByValue(self, value):
        "remove the list items with the value"

        currentNode = self.head
        previousNode = None

        while currentNode is not None:
            if currentNode.hasValue(value):
                # if this is the first node (head)
                if previousNode is not None:
                    previousNode.next = currentNode.next
                else:
                    self.head = currentNode.next
 
            # needed for the next iteration
            previousNode = currentNode
            currentNode = currentNode.next

        return

    def unorderedSearch (self, value):
        "search the linked list for the node that has this value"

        # define currentNode
        currentNode = self.head
        # define position
        nodeId = 1

        # define list of results
        results = []

        while currentNode is not None:
            if currentNode.hasValue(value):
                results.append(nodeId)
            
            # jump to the linked node
            currentNode = currentNode.getNext()
            nodeId = nodeId + 1
        
        return results

# main program

# create four single nodes
node1 = ListNode(15)
node2 = ListNode(8.2)
node3 = ListNode("Berlin")
node4 = ListNode(15)

track = SingleLinkedList()
print ("track length: %i" % track.listLength())

for currentNode in [node1, node2, node3, node4]:
    track.addListitem(currentNode)
    print ("track length: %i" % track.listLength())
    track.outputList()

# search for a certain value in the list
results = track.unorderedSearch (15)
if (len(results)):
    print (results)

# remove all the entries with value 15
track.removeListitemByValue(15)
track.outputList()

# remove the first list item
track.removeListitemById(1)
track.outputList()
