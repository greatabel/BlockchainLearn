import socket, pickle, random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, asymmetric
from i2mycrypto import MyCryptoLibrary
from termcolor import colored, cprint


# 密钥生成
alice_private_key = asymmetric.rsa.generate_private_key(
    public_exponent=65537, key_size=4096, backend=default_backend()
)
print("alice_private_key generated", alice_private_key, "#" * 20)
# 假设 Bob 有 Alice 的 PK，因此在 Bob 的共钥中将其保存为 PEM 格式
alice_key_pem = alice_private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

with open("PK_alice.pem", "wb") as key:
    key.write(alice_key_pem)


def retrieve_bobs_pk():
    with open("PK_bob.pem", "rb") as pem_file:
        PK = serialization.load_pem_public_key(
            pem_file.read(), backend=default_backend()
        )
        return PK


def decrypt_and_verify(data, PK):
    decrypted_message = MyCryptoLibrary.decrypt_message(data[0], alice_private_key)
    MyCryptoLibrary.verify_message(decrypted_message, data[1], PK)
    return decrypted_message


def send_encrypted_signed_message(msg, PK):
    cipher_text = MyCryptoLibrary.encrypt_message(msg, PK)
    signature_alice = MyCryptoLibrary.sign_message(msg, alice_private_key)
    data = (cipher_text, signature_alice)
    data_string = pickle.dumps(data)
    server.send(data_string)


def compute_dice_throw(a, b):
    dice_throw = bin(int(a) ^ int(b))
    converted_dice_throw = (int(dice_throw, 2) % 6) + 1
    print("Alice computes throw to be ", converted_dice_throw)
    return converted_dice_throw


# TCP with ipv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 6677
address = (host, port)

# Connect to address
server.connect(address)
running = True

text = colored(
    f"[Connected to {host} at port {port}]",
    "green",
    attrs=["reverse", "blink"],
)
print(text)


while running:
    # Get prerequisites
    PK_bob = retrieve_bobs_pk()

    print("********* Alice's dice throw *********")

    # [a1] Alice samples random bit a and random 128 bit string and sends Com(a,r)
    a1 = "1001"  # Alice not honest!!!!!!!!!!!!!!!!
    r1 = format(random.getrandbits(128), "b")
    c1 = bytes(a1 + r1, encoding="utf-8")
    c_hashed1 = MyCryptoLibrary.hash_message(c1)
    send_encrypted_signed_message(c_hashed1, PK_bob)
    print("Sending encrypted Com(a,r) to Bob")

    # [a2] Message b received
    received_data = pickle.loads(server.recv(2048))
    print("Alice received b from Bob and tries to verify")
    b1 = decrypt_and_verify(received_data, PK_bob)

    # [a3] Alice sends (a,r) to Bob
    a_r = bytes(a1 + "," + r1, encoding="utf-8")
    send_encrypted_signed_message(a_r, PK_bob)

    # [a4] Compute output a XOR b under mod 6
    compute_dice_throw(a1, b1)

    print()
    print("********* Bob's dice throw *********")

    # [a1] Message Com(a,r) received from Bob
    received_data2 = pickle.loads(server.recv(2048))
    print("Bob received Com(a,r) from Alice and tries to verify")
    decrypted_hashed_c_from_bob = decrypt_and_verify(received_data2, PK_bob)

    # [a2] Alice sends random bit a to Bob
    a2 = bytes(format(random.getrandbits(4), "b"), encoding="utf-8")
    send_encrypted_signed_message(a2, PK_bob)

    # [a3] Receive second message (a,r) from Bob
    received_data3 = pickle.loads((server.recv(2048)))
    print("Alice received (a,r) from Bob and tries to verify")
    decrypted_b_r = decrypt_and_verify(received_data3, PK_bob)
    decoded_split_b_r = decrypted_b_r.decode("utf-8").split(",")
    bob_b2 = decoded_split_b_r[0]
    opened_commitment = bytes(decoded_split_b_r[0] + decoded_split_b_r[1], "utf-8")

    # [a4] Alice is hashing a + r for checking and computing dice throw
    opened_commitment_hashed = MyCryptoLibrary.hash_message(opened_commitment)

    if decrypted_hashed_c_from_bob == opened_commitment_hashed:
        print("Alice is checking if the hashes match")
        print("[Success] No changes we made to the message")
        bob_b = decoded_split_b_r[0]
        alice_a = a2.decode("utf-8")
        compute_dice_throw(alice_a, bob_b)
    else:
        print("[WARNING] Bob changed his message")

    running = False

server.close()
