import sys
import socket
import threading
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
import os
import gen_key

HOST = '127.0.0.1'
PORT = 65432

try:
    with open("server_public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
except FileNotFoundError:
    gen_key.generateKeyPair()
    with open("server_public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

aes_key = os.urandom(32)  # 256 bits
iv = os.urandom(16)  # 128 bits

encrypted_aes_key = public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send(encrypted_aes_key)
client.send(iv)  # Enviar IV al servidor

def receive_messages():
    while True:
        try:
            aes_cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            decryptor = aes_cipher.decryptor()
            unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()

            encrypted_message = client.recv(1024)
            if not encrypted_message:
                break

            decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
            unpadded_message = unpadder.update(decrypted_message) + unpadder.finalize()
            print(f"{unpadded_message.decode()}")

        except Exception as e:
            print(f"Error receiving message: {e}")
            client.close()
            break

def send_messages():
    nickname = input("Choose a nickname: ")
    while True:
        try:
            aes_cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            encryptor = aes_cipher.encryptor()
            padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()

            message = input(f"{nickname}: ")
            formatted_message = f"{nickname}: {message}"
            padded_message = padder.update(formatted_message.encode()) + padder.finalize()
            encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
            client.send(encrypted_message)

        except Exception as e:
            print(f"Error sending message: {e}")
            client.close()
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
