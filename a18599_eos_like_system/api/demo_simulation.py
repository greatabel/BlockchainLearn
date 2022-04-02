from http import HTTPStatus
from flask import Blueprint, abort
from flasgger import swag_from
from api.globals import blockchain
from api.schema.blockchain import BlockchainSchema
from api.schema.block import BlockSchema

from blockchain.block import Block

demo_simulation_api = Blueprint('demo_simulation', __name__)


@demo_simulation_api.route('/simulate')
def simulate():
   	print('invoke simulate', '#'*20)
   	block = Block(1, [], 0, '0')
   	print('测试eos-like区块：', block.hash, block.hash_block())
   	print('加入区块链的区块为：',  block.hash_block())
   	return {"msg":"simulate!"}, 200