import requests
import time
from flask import Flask, jsonify, request

from api.dpos_blockchain import DPOS_Blockchain

from flask import Blueprint, abort
from termcolor import colored, cprint


# 用blueprint类标识符初始化我们的节点并实例化区块链类
dpos_blockchain_api = Blueprint("dpos_simulation", __name__)

blockchain = DPOS_Blockchain()

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-p', '--port', default=4999, type=int, help='Listening on port')
args = parser.parse_args()
port = args.port


@dpos_blockchain_api.route("/simulate")
def simulate():
    welcome = colored(
        "--------- dpos_blockchain_api: simulate ----------",
        "blue",
        attrs=["reverse", "blink"],
    )
    print(welcome)

    step1 = colored(
        "---------step1 dpos_blockchain simulate nodes adding----------",
        "blue",
        attrs=["reverse", "blink"],
    )
    print(step1)

    print('simulate node 1')
    # Update an existing resource
    json_data = {
                'nodes': 'http://localhost:4999',
                'stake': 31
                }
    add_api = 'http://localhost:4999/api/dpos/nodes/add'
    response = requests.post(url = add_api, json=json_data)
    print('dpos-eos-like-system 请求回应为:', response.text)

    time.sleep(1.5)
    print('simulate node 2')
    json_data = {
                'nodes': 'http://localhost:5010',
                'stake': 50
                }
    add_api = 'http://localhost:4999/api/dpos/nodes/add'
    response = requests.post(url = add_api, json=json_data)
    print('dpos-eos-like-system 请求回应为:', response.text)

    time.sleep(1.5)
    print('simulate node 3')
    json_data = {
                'nodes': 'http://localhost:5011',
                'stake': 51
                }
    add_api = 'http://localhost:4999/api/dpos/nodes/add'
    response = requests.post(url = add_api, json=json_data)
    print('dpos-eos-like-system 请求回应为:', response.text)

    time.sleep(1.5)
    print('simulate node 4')
    json_data = {
                'nodes': 'http://localhost:5012',
                'stake': 52
                }
    add_api = 'http://localhost:4999/api/dpos/nodes/add'
    response = requests.post(url = add_api, json=json_data)
    print('dpos-eos-like-system 请求回应为:', response.text)

    step2 = colored(
        "---------step2 dpos_blockchain simulate node voting---------",
        "blue",
        attrs=["reverse", "blink"],
    )
    print(step2)
    time.sleep(2)

    voting_api = 'http://localhost:4999/api/dpos/voting'
    response = requests.get(url = voting_api)
    print('dpos-eos-like-system 请求回应为:', response.text)
    time.sleep(2)

    step3 = colored(
        "---------step3 dpos_blockchain simulate node delegate show----------",
        "blue",
        attrs=["reverse", "blink"],
    )
    print(step3)
    delegate_show_api = 'http://localhost:4999/api/dpos/delegates/show'
    response = requests.get(url = delegate_show_api)
    print('dpos-eos-like-system 请求回应为:', response.text)

    step4 = colored(
        "---------step4 dpos_blockchain simulate new transaction ----------",
        "blue",
        attrs=["reverse", "blink"],
    )
    print(step4)
    json_data = {
                'user_name': 'abel',
                'item_name': 'Bounty Item NFT Demo',
                'billing_value': 101
                }
    transactions_new_api = 'http://localhost:4999/api/dpos/transactions/new'
    response = requests.post(url = transactions_new_api, json=json_data)
    print('dpos-eos-like-system 请求回应为:', response.text)
    time.sleep(1.5)

    json_data = {
                'user_name': 'zaiye',
                'item_name': 'Bounty Item NFT Demo',
                'billing_value': 110
                }
    transactions_new_api = 'http://localhost:4999/api/dpos/transactions/new'
    response = requests.post(url = transactions_new_api, json=json_data)
    print('dpos-eos-like-system 请求回应为:', response.text)
    time.sleep(1.5)


    step5 = colored(
        "---------step5 dpos_blockchain simulate mining----------",
        "blue",
        attrs=["reverse", "blink"],
    )
    print(step5)
    mine_api = 'http://localhost:4999/api/dpos/mine'
    response = requests.get(url = mine_api)
    print('dpos-eos-like-system mining回应为:', response.text)

    return {"msg": "dpos simulate!"}, 200


# 挖矿dpos
@dpos_blockchain_api.route("/mine", methods=["GET"])
# Method to mine a block
def mine():
    # port = 4999
    global port

    current_port = "localhost:" + str(port)
    if current_port in blockchain.delegates:

        # 需要至少初始2节点
        if len(blockchain.unverified_transactions) >= 2:
            last_block = blockchain.last_block
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(previous_hash)

            response = {
                "message": "New block mined!",
                "index": block["index"],
                "transactions": block["transactions"],
                "previous_hash": block["previous_hash"],
            }
            print(len(blockchain.unverified_transactions))
            return jsonify(response), 200

        else:
            response = {
                "message": "Not enough transactions to mine a new block and add to chain!"
            }
            print(len(blockchain.unverified_transactions))
            return jsonify(response), 400
    else:
        response = {
            "message": "You are not authorised to mine block! Only delegates can mine."
        }
        return jsonify(response), 400



@dpos_blockchain_api.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()

    required = ["user_name", "item_name", "billing_value"]
    if not all(k in values for k in required):
        return (
            "Missing values! Please enter user_name, item_name and billing amount.",
            400,
        )

    index = blockchain.new_transaction(
        values["user_name"], values["item_name"], values["billing_value"]
    )

    response = {"message": f"Transaction will be added to block {index}"}
    return jsonify(response), 201



@dpos_blockchain_api.route("/chain", methods=["GET"])
def full_chain():
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    return jsonify(response), 200


# 用于添加新节点的 HTTP 地址及其在网络中的股份的节点
@dpos_blockchain_api.route("/nodes/add", methods=["POST"])
def add_nodes():
    values = request.get_json()
    required = ["nodes", "stake"]

    if not all(k in values for k in required):
        return "Error", 400

    blockchain.add_node(values["nodes"], values["stake"])

    response = {
        "message": "New nodes are added!",
        "total_nodes": list(blockchain.nodes),
    }
    print(blockchain.nodes)
    return jsonify(response), 201


# 开启投票
@dpos_blockchain_api.route("/voting", methods=["GET"])
def voting():
    print('port:', port)
    if port == 4999:
        show_votes = blockchain.add_vote()

        response = {
            "message": "The voting results are as follows:",
            "nodes": blockchain.voteNodespool,
        }

        return jsonify(response), 200

    else:
        response = {
            "message": "You are not authorized to conduct the election process!"
        }
        return jsonify(response), 400


# 代理节点展示
@dpos_blockchain_api.route("/delegates/show", methods=["GET"])
def delegates():
    show_delegates = blockchain.selection()

    response = {
        "message": "3 choosed nodes as delegates are:",
        "node_delegates": blockchain.delegates,
    }
    return jsonify(response), 200


# 与网络中所有其他节点同步当选代表名单的端点
@dpos_blockchain_api.route("/delegates/sync", methods=["GET"])
def sync_delegates():
    sync_delegates = blockchain.sync()

    response = {
        "message": "delegate nodes are:",
        "node_delegates": blockchain.delegates,
    }
    return jsonify(response), 200


# 用最长的验证链解决和替换当前链的端点，达成共识
@dpos_blockchain_api.route("/chain/resolve", methods=["GET"])
def consensus():
    replaced = blockchain.resolve_chain()

    if replaced:
        response = {"message": "Our chain was replaced", "new_chain": blockchain.chain}
    else:
        response = {"message": "Our chain is authoritative", "chain": blockchain.chain}
    return jsonify(response), 200


