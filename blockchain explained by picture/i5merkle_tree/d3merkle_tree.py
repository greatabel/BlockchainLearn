import hashlib

class MerkleNode:
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data


def createTree(nodes):
    list_len = len(nodes)
    if list_len == 0:
        return 0
    else:
        while list_len %2 != 0:
            nodes.extend(nodes[-1:])
            list_len = len(nodes)
        secondary = []
        #combine 2 nodes in pair
        for k in [nodes[x: x+2] for x in range(0, list_len, 2)]:
            d1 = k[0].data.encode('utf-8')
            d2 = k[1].data.encode('utf-8')
            sha = hashlib.sha256()
            sha.update(d1 + d2)
            newdata = sha.hexdigest()
            print(d1, d2 , ' newdata=', newdata)

if __name__ == "__main__":
    blocks = ['A','B','C','D','E']
    nodes = []
    print('叶子节点的hash:')
    for e in blocks:
        sha = hashlib.sha256()
        sha.update(e.encode('utf-8'))
        d = sha.hexdigest()
        nodes.append(MerkleNode(data=d))
        print(e + ' 叶子节点 ' + d)
    print('-'*30)
    root = createTree(nodes)