import socket
import threading
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as pad
import sys

host = "127.0.0.1"

if len(sys.argv) == 2:
    host = sys.argv[1]


# Load server's public key
def load_server_public_key():
    with open("server_public_key.pem", "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

# Load client's private key
def load_client_private_key():
    with open("client_private_key.pem", "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)

def encrypt_message(message, public_key):
    aes_key = os.urandom(32)
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB())
    encryptor = cipher.encryptor()
    padder = pad.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    return encrypted_aes_key, encrypted_message

def decrypt_message(encrypted_message, aes_key):
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    unpadder = pad.PKCS7(algorithms.AES.block_size).unpadder()
    return unpadder.update(decrypted_message) + unpadder.finalize()

# Setup
nickname = input("Choose your nickname: ")
server_public_key = load_server_public_key()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

# Send nickname to server
client.send(nickname.encode('ascii'))

# Listening to server and sending nickname
def receive():
    while True:
        try:
            encrypted_message = client.recv(1024)
            if not encrypted_message:
                print("Connection closed by server.")
                break
            aes_key = load_client_private_key().decrypt(
                encrypted_message[:256],
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            decrypted_message = decrypt_message(encrypted_message[256:], aes_key)
            print(decrypted_message.decode())
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

# Sending messages to server
def write():
    while True:
        message = input('')
        encrypted_aes_key, encrypted_message = encrypt_message(message, server_public_key)
        client.send(encrypted_aes_key + encrypted_message)

# Starting threads for receiving and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
