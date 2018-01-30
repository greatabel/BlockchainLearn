from Crypto.PublicKey import RSA

secret_code = "This is Abel's secret"
key = RSA.generate(2048)
encrypted_key = key.exportKey(passphrase=secret_code,
                              pkcs=8,
                              protection="scryptAndAES128-CBC")

file_out = open("d4rsa_key.bin", "wb")
file_out.write(encrypted_key)

print(key.publickey().exportKey())
