""" Bob (localhost) """
import socket, pickle, random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, asymmetric
from MyCryptoLibrary import MyCryptoLibrary

# Key generation
bob_private_key = asymmetric.rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend())

# Assuming that Alice has bob's PK, thus saving it as PEM format to Alice's PC.
bob_key_pem = bob_private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)

with open("PK_bob.pem", "wb") as key:
    key.write(bob_key_pem)


def retrieve_alice_pk():
    with open("PK_alice.pem", "rb") as pem_file:
        PK = serialization.load_pem_public_key(
            pem_file.read(),
            backend=default_backend())
        return PK


def decrypt_and_verify(data, PK):
    decrypted_message = MyCryptoLibrary.decrypt_message(data[0], bob_private_key)
    MyCryptoLibrary.verify_message(decrypted_message, data[1], PK)
    return decrypted_message


def send_encrypted_signed_message(msg, PK):
    cipher_text = MyCryptoLibrary.encrypt_message(msg, PK)
    signature_alice = MyCryptoLibrary.sign_message(msg, bob_private_key)
    data = (cipher_text, signature_alice)
    data_string = pickle.dumps(data)
    client_socket.send(data_string)


def compute_dice_throw(b, a):
    dice_throw = bin(int(b) ^ int(a))
    converted_dice_throw = (int(dice_throw, 2) % 6) + 1
    print("Bob computes throw to be ", converted_dice_throw)
    return converted_dice_throw


# TCP socket with ipv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"; port = 6677
address = (host, port)
server.bind(address)

# Handle connections
server.listen(2048)
running = True
print(f"[Server started at {host} on port {port}]")

# Creating the message to send

while running:
    # Accept connection from client
    client_socket, address = server.accept()
    print(f"Connection from {address} has been established...")

    # Get prerequisites
    PK_alice = retrieve_alice_pk()

    print("********* Alice's dice throw *********")

    # [b1] Message Com(a,r) received from alice
    received_data = pickle.loads(client_socket.recv(2048))
    print("Bob received Com(a,r) from Alice and tries to verify")
    decrypted_hashed_c_from_alice = decrypt_and_verify(received_data, PK_alice)

    # [b2] Bob sends random bit b to Alice
    b1 = bytes(format(random.getrandbits(4), "b"), encoding="utf-8")
    send_encrypted_signed_message(b1, PK_alice)

    # [b3] Receive second message (a,r) from Alice
    received_data2 = pickle.loads((client_socket.recv(2048)))
    print("Bob received (a,r) from Alice and tries to verify")
    decrypted_a_r = decrypt_and_verify(received_data2, PK_alice)
    decoded_split_a_r = decrypted_a_r.decode("utf-8").split(",")
    alice_a1 = decoded_split_a_r[0]
    opened_commitment = bytes(decoded_split_a_r[0] + decoded_split_a_r[1], "utf-8")

    # [b4] Bob is hashing a + r for checking and computing dice throw
    opened_commitment_hashed = MyCryptoLibrary.hash_message(opened_commitment)

    if decrypted_hashed_c_from_alice == opened_commitment_hashed:
        print("Bob is checking if the hashes match")
        print("[Success] No changes we made to the message")
        alice_a = decoded_split_a_r[0]
        bob_b = b1.decode("utf-8")
        compute_dice_throw(bob_b, alice_a)
    else:
        print("[WARNING] Alice changed her message")

    print()
    print("********* Bob's dice throw *********")

    # [b1] Bob samples random bit b and random 128 bit string and sends Com(a,r)
    b2 = format(random.getrandbits(4), "b")
    r2 = format(random.getrandbits(128), "b")
    c2 = bytes(b2 + r2, encoding="utf-8")
    c_hashed2 = MyCryptoLibrary.hash_message(c2)
    send_encrypted_signed_message(c_hashed2, PK_alice)
    print("Sending encrypted Com(a,r) to Alice")

    # [b2] Message a received
    received_data3 = pickle.loads(client_socket.recv(2048))
    print("Alice received b from Bob and tries to verify")
    a2 = decrypt_and_verify(received_data3, PK_alice)

    # [b3] Bob sends (a,r) to Alice
    b_r = bytes(b2 + "," + r2, encoding="utf-8")
    send_encrypted_signed_message(b_r, PK_alice)

    # [b4] Compute output B XOR a under mod 6
    compute_dice_throw(b2, a2)

    running = False

client_socket.close()


