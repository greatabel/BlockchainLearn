import hashlib
import json
from datetime import datetime
from urllib.parse import urlparse
import requests
from random import randint

# dpos Blockchain class
class DPOS_Blockchain(object):

    # 创建列表以存储 DPOS 区块链和交易的构造函数
    def __init__(self):

        self.chain = []

        self.unverified_transactions = []

        self.verified_transactions = []

        # Genesis block
        self.new_block(previous_hash=1)

        # 包含网络中节点的集合。 在此处使用 set 以防止再次添加相同的节点。
        self.nodes = set()

        # 包含所有节点及其在网络中的股份的列表
        self.all_nodes = []

        # 投票节点池
        self.voteNodespool = []

        # 按收到的票数降序存储所有节点的列表
        self.starNodespool = []

        # 存储前 3 个最高节点的列表 (stake * votes_received)
        self.superNodespool = []

        # 存储选择用于挖掘过程的委托节点地址的列表
        self.delegates = []

    # 在 DPOS 区块链中创建新区块的方法
    def new_block(self, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transactions": self.unverified_transactions,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }
        self.verified_transactions += self.unverified_transactions
        print(self.verified_transactions)
        self.unverified_transactions = []

        # appending the block at the end of the DPOS Blockchain
        self.chain.append(block)
        return block

    # 在下一个区块中添加新交易的方法
    def new_transaction(self, sender, item_name, bill_amount):
        self.unverified_transactions.append(
            {
                "shop simulate username": sender,
                "accepter": "dpos EOS Like System",
                "item": item_name,
                "bidding value": bill_amount,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        return self.last_block["index"] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    # Static method to create a SHA-256 Hash of a given block
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        hash_val = hashlib.sha256(block_string).hexdigest()
        return hash_val

    def add_node(self, address, stake):
        parsed_url = urlparse(address)
        authority = stake
        self.nodes.add((parsed_url.netloc, authority))

    def add_vote(self):
        self.all_nodes = list(self.nodes)

        for x in self.all_nodes:
            y = list(x)
            y.append(x[1] * randint(0, 100))
            self.voteNodespool.append(y)

        print(self.voteNodespool)

    def selection(self):
        self.starNodespool = sorted(
            self.voteNodespool, key=lambda vote: vote[2], reverse=True
        )
        print(self.starNodespool)

        for x in range(3):
            self.superNodespool.append(self.starNodespool[x])
        print(self.superNodespool)

        for y in self.superNodespool:
            self.delegates.append(y[0])
        print(self.delegates)

    # 同步到list
    def sync(self):
        port = "4999"
        r = requests.get("http://localhost:" + port + "/api/dpos/delegates/show")
        print(r)

        if r.status_code == 200:
            delegates = r.json()["node_delegates"]
            self.delegates = delegates[0:3]
            print(self.delegates)

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            # If the hash value of the current block isn't correct then return false
            if block["previous_hash"] != self.hash(last_block):
                return False

            last_block = block
            current_index += 1

        return True

    # 用网络中最长的验证链替换 DPOS 区块链的方法。
    def resolve_chain(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f"http://{node}/chain")

            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False
