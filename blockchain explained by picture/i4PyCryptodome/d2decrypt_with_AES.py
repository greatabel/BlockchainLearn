from Crypto.Cipher import AES


# https://pycryptodome.readthedocs.io/en/latest/src/examples.html#encrypt-data-with-aes
file_in = open('d1_encrypted.bin', "rb")
nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
print(nonce, tag, ciphertext)
# let's assume that the key is somehow available again
key= b"B\x04\x11'\xcb\xd6\x18 \xf4\x97H\xb2\xd7\xf3\xe1\x0c"

cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)
print('data=', data)