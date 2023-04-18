from ecdsa import SigningKey, SECP256k1

sk = SigningKey.generate(curve=SECP256k1)
pk = sk.verifying_key

with open("private_key.pem", "wb") as f:
    f.write(sk.to_pem())

with open("public_key.pem", "wb") as f:
    f.write(pk.to_pem())
