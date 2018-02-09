from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

data = b"test_content"

key = get_random_bytes(16)
print("key=", key)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)
file_out = open("d1_encrypted.bin", "wb")
[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]