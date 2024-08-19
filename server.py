import socket
import threading
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as pad

# Load server's private key
def load_server_private_key():
    with open("server_private_key.pem", "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)

# Load client's public key
def load_client_public_key():
    with open("client_public_key.pem", "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

def decrypt_message(encrypted_message, aes_key):
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    unpadder = pad.PKCS7(algorithms.AES.block_size).unpadder()
    return unpadder.update(decrypted_message) + unpadder.finalize()

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
    return encrypted_aes_key + encrypted_message

host = "127.0.0.1"
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            client.close()
            clients.remove(client)

def handle(client):
    while True:
        try:
            encrypted_message = client.recv(1024)
            if not encrypted_message:
                break
            aes_key = load_server_private_key().decrypt(
                encrypted_message[:256],
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            decrypted_message = decrypt_message(encrypted_message[256:], aes_key)
            broadcast(decrypted_message)
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            clients.remove(client)
            break

def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request and store nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
