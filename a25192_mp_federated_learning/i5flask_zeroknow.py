from flask import Flask, request, jsonify
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import base64
from ecdsa import VerifyingKey, SECP256k1

pk = None
with open("public_key.pem", "rb") as f:
    pk = VerifyingKey.from_pem(f.read())

app = Flask(__name__)


@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    b = data["b"]
    msg = b"Hello, world!"
    
    if b == 0:
        signature = base64.b64decode(data["signature"])
        result = pk.verify(signature, msg)
    else:
        msg = b"Hello, world!"
        signature = base64.b64decode(data["signature"])
        result = pk.verify(signature, msg)

    if result:
        return jsonify({"result": "Verification succeeded"})
    else:
        return jsonify({"result": "Verification failed"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
