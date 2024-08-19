import socket
import threading
import secrets
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as pad
import gen_key

HOST = 'localhost'
PORT = 5555
LISTENER_LIMIT = 5
active_clients = {}  # Store clients and their keys

def load_public_key():
    try:
        with open("server_public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
    except FileNotFoundError:
        gen_key.generateKeyPair()
        with open("server_public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
    return public_key

def load_private_key():
    return gen_key.load_private_key()

def broadcast_message(message):
    for client, _ in active_clients.values():
        try:
            client.sendall(message)
        except Exception as e:
            print(f"Error sending message to client: {e}")

def handle_client(conn, aes_key):
    aes_cipher = Cipher(algorithms.AES(aes_key), modes.ECB())
    decryptor = aes_cipher.decryptor()
    encryptor = aes_cipher.encryptor()

    def receive_messages():
        while True:
            try:
                encrypted_message = conn.recv(4096)
                if not encrypted_message:
                    print("Connection closed by client.")
                    break
                decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
                unpadder = pad.PKCS7(algorithms.AES.block_size).unpadder()
                decrypted_message = unpadder.update(decrypted_message) + unpadder.finalize()
                print(f"Client: {decrypted_message.decode()}")
                broadcast_message(encrypted_message)  # Broadcast to all clients
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        conn.close()
        del active_clients[conn]  # Remove client from active_clients

    def send_messages():
        while True:
            try:
                message = input("You: ")
                if message.lower() == 'exit':
                    break
                padder = pad.PKCS7(algorithms.AES.block_size).padder()
                padded_message = padder.update(message.encode()) + padder.finalize()
                encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
                conn.sendall(encrypted_message)
            except Exception as e:
                print(f"Error sending message: {e}")
                break
        conn.close()

    threading.Thread(target=receive_messages, daemon=True).start()
    threading.Thread(target=send_messages, daemon=True).start()

def start_server():
    public_key = load_public_key()
    private_key = load_private_key()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(LISTENER_LIMIT)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        encrypted_aes_key = conn.recv(1024)
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("AES key received and decrypted")
        active_clients[conn] = (conn, aes_key)
        handle_client(conn, aes_key)

if __name__ == "__main__":
    start_server()
