from flask import Flask, request, jsonify, render_template
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import base64
from ecdsa import VerifyingKey, SECP256k1

pk = None
with open("public_key.pem", "rb") as f:
    pk = VerifyingKey.from_pem(f.read())

app = Flask(__name__)


@app.route("/verify", methods=["POST", "GET"])
def verify():
    if request.method == "GET":
        return render_template("form.html")
    b = request.form["b"]
    signature  = request.form["signature"]
    print('b==', b, signature)


    msg = b"Hello, world!"
    try:
        if b == 0:
                signature = base64.b64decode(request.form["signature"])
                result = pk.verify(signature, msg)
        else:
            msg = b"Hello, world!"
            signature = base64.b64decode(request.form["signature"])
            result = pk.verify(signature, msg)

        if result:
            return render_template("result.html", result="Verification succeeded")
        else:
            return render_template("result.html", result="Verification failed"), 400
    except:
        return render_template("result.html", result="Verification failed"), 400

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)