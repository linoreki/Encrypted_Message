import sys
import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import gen_key

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


aes_key = os.urandom(32)  

encrypted_aes_key = public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

client.send(encrypted_aes_key)

aes_cipher = Cipher(algorithms.AES(aes_key), modes.ECB())
encryptor = aes_cipher.encryptor()

def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)
    
def receive_messages():
    while True:
        try:
            encrypted_message = client.recv(1024)
            decrypted_message = aes_cipher.decryptor().update(encrypted_message)
            print(f"Server: {decrypted_message.decode()}")
        except:
            print("Error receiving message")
            client.close()
            break

def send_messages():
    while True:
        message = input("")
        encrypted_message = encryptor.update(message.encode())
        client.send(encrypted_message)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
