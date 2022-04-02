from flask import Flask
from flask_marshmallow import Marshmallow
from flasgger import Swagger
from api.home import api
from api.blockchain import blockchain_api
from api.miner import miner_api
from api.transaction import transaction_api


def create_app():
    app = Flask(__name__)
    return app


app = create_app()
ma = Marshmallow(app)

app.config["SWAGGER"] = {
    "title": "Blockchain API",
}
swagger = Swagger(app)


app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(blockchain_api, url_prefix="/api/blockchain")
app.register_blueprint(miner_api, url_prefix="/api/miner")
app.register_blueprint(transaction_api, url_prefix="/api/transaction")


if __name__ == "__main__":
    print('EOS Like Blockchain is running...')
    port = 4999
    app.debug = True
    app.run(host="127.0.0.1", port=port)
