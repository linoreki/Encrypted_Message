Encrypted Messenger with RSA and AES
Overview
This project is an encrypted messaging application built with Python, utilizing RSA for secure key exchange and AES for encrypted communication. It features a client-server architecture where messages between clients are securely transmitted through a central server.

Features
RSA Key Exchange: RSA encryption is used to securely exchange AES keys between the client and server.
AES Encryption: AES encryption is used for securing the actual message communication.
Multi-client Support: The server can handle multiple clients simultaneously.
Threaded Communication: Each client connection is handled in a separate thread to ensure smooth and simultaneous communication.
Installation
Clone the repository:

bash
Copiar código
git clone https://github.com/your-username/encrypted-messenger.git
cd encrypted-messenger
Install dependencies:
Ensure you have Python installed, and then install the required Python packages:

bash
Copiar código
pip install cryptography
Generate RSA keys:
Before running the server, you need to generate RSA keys for encryption and decryption. You can do this with the following Python script:

python
Copiar código
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Save the private key to a file
with open("server_private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Generate the corresponding public key
public_key = private_key.public_key()

# Save the public key to a file
with open("server_public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))
Run this script to generate the server_private_key.pem and server_public_key.pem files.

Usage
Running the Server
Start the server:

bash
Copiar código
python server.py
The server will start listening for incoming client connections on localhost at port 5555.

Running the Client
Start the client:

bash
Copiar código
python client.py
The client will connect to the server, generate an AES key, encrypt it using the server's public RSA key, and send the encrypted AES key to the server. The client can then send and receive encrypted messages.

Multi-client Communication
You can run multiple instances of client.py to simulate multiple users connecting to the server. Each client will be able to send and receive messages securely.

Project Structure
server.py: The main server script that handles incoming client connections and message broadcasting.
client.py: The client script that connects to the server, exchanges keys, and handles encrypted communication.
server_private_key.pem: The RSA private key used by the server to decrypt the AES key sent by the client.
server_public_key.pem: The RSA public key used by clients to encrypt the AES key before sending it to the server.
Future Enhancements
Use CBC Mode with IV: Implement AES encryption using CBC mode with an initialization vector (IV) for stronger security.
Key Rotation: Implement a key management system for periodic rotation of AES keys.
User Authentication: Add a simple authentication system to verify the identity of clients and the server.
License
This project is licensed under the MIT License. See the LICENSE file for details.
