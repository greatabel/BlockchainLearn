from flask import Flask
from flask_marshmallow import Marshmallow
from flasgger import Swagger
from api.home import api
from api.blockchain import blockchain_api
from api.miner import miner_api
from api.transaction import transaction_api
from api.demo_simulation import demo_simulation_api
# from api.dpos_simulation import dpos_blockchain_api

from argparse import ArgumentParser


def create_eos_like_app():
    eos_like_app = Flask(__name__)
    return eos_like_app


eos_like_app = create_eos_like_app()
ma = Marshmallow(eos_like_app)

eos_like_app.config["SWAGGER"] = {
    "title": "EOS-like Blockchain API",
}
swagger = Swagger(eos_like_app)


eos_like_app.register_blueprint(api, url_prefix="/api")
eos_like_app.register_blueprint(blockchain_api, url_prefix="/api/blockchain")
eos_like_app.register_blueprint(miner_api, url_prefix="/api/miner")
eos_like_app.register_blueprint(transaction_api, url_prefix="/api/transaction")
eos_like_app.register_blueprint(demo_simulation_api, url_prefix="/api/demo_simulation")

# dpos
# eos_like_app.register_blueprint(dpos_blockchain_api, url_prefix="/api/dpos")

if __name__ == "__main__":
    print("EOS Like Blockchain is running...")

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=4999, type=int, help="Listening on port"
    )
    args = parser.parse_args()
    port = args.port

    # port = 4999
    eos_like_app.debug = True
    eos_like_app.run(host="127.0.0.1", port=port)
