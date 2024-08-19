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
    with open("server_private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
except FileNotFoundError:
    gen_key.generateKeyPair()
    with open("server_private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error broadcasting message to client: {e}")
                client.close()
                clients.remove(client)

def handle_client(client):
    try:
        # Recibir la clave AES encriptada
        encrypted_aes_key = client.recv(256)
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Recibir IV
        iv = client.recv(16)

        while True:
            # Recibir mensaje encriptado
            encrypted_message = client.recv(1024)
            if not encrypted_message:
                break

            aes_cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            decryptor = aes_cipher.decryptor()
            unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()

            decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
            unpadded_message = unpadder.update(decrypted_message) + unpadder.finalize()

            message_text = unpadded_message.decode()
            print(f"Received: {message_text}")

            # Reenviar mensaje a otros clientes
            broadcast(encrypted_message, client)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        if client in clients:
            clients.remove(client)
        client.close()

def receive_connections():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is listening...")
receive_connections()
