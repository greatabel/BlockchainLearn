# David Chaum 1983 提出加密技术运用于现金
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

# sender can create the signatue of a message using their private key
message = b"To be signed"
key = RSA.importKey(
    open("../01blockchain explained by picture/i4PyCryptodome/d3private.pem").read()
)
h = SHA256.new(message)
signature = pss.new(key).sign(h)

print(signature, type(signature))

print("-" * 20)

key = RSA.importKey(
    open("../01blockchain explained by picture/i4PyCryptodome/d3public.pem").read()
)
h = SHA256.new(message)
verifier = pss.new(key)
try:
    verifier.verify(h, signature)
    print("The signature is authentic.")
except (ValueError, TypeError):
    print("The signature is not authentic.")
