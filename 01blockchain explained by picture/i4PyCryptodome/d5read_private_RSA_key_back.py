from Crypto.PublicKey import RSA

# secret_code = "Unguessable" # which is wrong
secret_code = "This is Abel's secret"
encoded_key = open("d4rsa_key.bin", "rb").read()
key = RSA.import_key(encoded_key, passphrase=secret_code)

print(key.publickey().exportKey())