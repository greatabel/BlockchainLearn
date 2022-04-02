from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from
from api.globals import blockchain
from api.schema.miner import MineSchema

miner_api = Blueprint('miner', __name__)


@miner_api.route('/mine', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'The block with all its transactions.',
            'schema': MineSchema
        }
    }
})
def mine():
    print('bgin mining new eos-block...', '#'*20)
    block = blockchain.mine('address')

    response = {
        'message': "New Block Mined",
        'block': block
    }

    return MineSchema().dumps(response), 200
