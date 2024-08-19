import socket
import sys
import threading
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import Key_Generate

try:
    with open("server_public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
except FileNotFoundError:
    Key_Generate.generateKeyPair()
    with open("server_public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen()

clients = []

def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def handle_client(client):
    while True:
        try:
            encrypted_aes_key = client.recv(256)
            aes_key = private_key.decrypt(
                encrypted_aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Now we can use the AES key for further communication
            aes_cipher = Cipher(algorithms.AES(aes_key), modes.ECB())
            decryptor = aes_cipher.decryptor()

            while True:
                encrypted_message = client.recv(1024)
                decrypted_message = decryptor.update(encrypted_message)
                print(f"Received: {decrypted_message.decode()}")
                broadcast(encrypted_message, client)
        except:
            clients.remove(client)
            client.close()
            break

def receive_connections():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is listening...")
receive_connections()
