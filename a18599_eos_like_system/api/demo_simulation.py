from http import HTTPStatus
from flask import Blueprint, abort
from flasgger import swag_from
from api.globals import blockchain
from api.schema.blockchain import BlockchainSchema
from api.schema.block import BlockSchema

from blockchain.block import Block
from blockchain import Blockchain


from termcolor import colored, cprint

demo_simulation_api = Blueprint('demo_simulation', __name__)


@demo_simulation_api.route('/simulate')
def simulate():
   	print('invoke simulate', '#'*20)
   	block = Block(1, [], 0, '0')
   	print('1.测试eos-like区块：', block.hash, block.hash_block())
   	print('1.加入eos-lik区块链的区块为：',  block.hash_block())


   	return {"msg":"simulate!"}, 200


@demo_simulation_api.route('/simulate_miner')
def simulate_miner():
   	print('invoke simulate_miner', '#'*20)
   	miner_address = 'miner_address'
   	blockchain = Blockchain()
   	blockchain.create_transaction('sender', 'recipient', 1)
   	blockchain.create_transaction('sender2', 'recipient2', 1.5)
   	print(len(blockchain.pending_transactions), 2)

   	block = blockchain.mine(miner_address)



    # Let's see if the block was added to the chain
   	print(blockchain.last_block.hash, block.hash)

    # We need to check that the transaction list is empty
   	print(0, len(blockchain.pending_transactions))

    # We need to check that the block contains all of the transactions
   	print(3, len(block.transactions))

   	reward_transaction = block.transactions[-1]

    # We make sure the reward function has no sender, and gives away exactly 1 coin
   	print('0', reward_transaction.sender)
   	print(miner_address, reward_transaction.recipient)
   	print(1, reward_transaction.amount)

   	
   	return {"msg":"simulate miner!"}, 200