# Encrypted_Message

Encrypted_Message is a simple messaging system that uses sockets for communication between a client and a server. This project also includes RSA key generation and management to secure the communication.

## Features

- Client-server communication using TCP sockets.
- RSA key generation for encrypting and decrypting messages.
- Support for multiple clients connected simultaneously.
- Management system for authorized public keys.

## Project Structure
- `clientGUI.py`: Client code that connects to the server, sends, and receives messages but with GUI.
- `client.py`: Client code that connects to the server, sends, and receives messages.
- `server.py`: Server code that handles client connections and relays messages between them.
- `gen_key.py`: Script to generate RSA keys for the server and clients.
- `add_key.py`: Script to add public keys to the server's authorized keys file.
- `test.py`: Test script to verify encryption and decryption functionality using the generated keys.
- `main.py`: Script to run all services in a GUI interface.

## Requirements

- Python 3.x
- `pycryptodome` library for RSA key generation and management.

You can install the required library with:

```bash
pip install pycryptodome
```

## Setup and Usage

1. **Generate RSA Keys**
   First, generate RSA keys for the server and clients:

   ```bash
   python gen_key.py
   ```

   This will generate the following keys:

   - Server keys: `server/key_private.pem` and `server/key_public.pem`
   - Client keys: `client/key_private.pem` and `client/key_public.pem`

2. **Add Authorized Public Keys**
   To authorize a client, add its public key to the server's list of allowed keys:

   ```bash
   python server/add_key.py client/key_public.pem server/allowed_keys.txt
   ```

3. **Run the Server**
   Start the server to listen for incoming connections:

   ```bash
   python server.py
   ```

4. **Connect a Client**
   Start a client and connect it to the server:

   ```bash
   python client.py [Server_IP_Address]
   ```

   If no IP address is specified, `127.0.0.1` (localhost) will be used by default.

5. **Test Encryption/Decryption**
   You can test the encryption and decryption process using the `test.py` script:

   ```bash
   python test.py
   ```

   This will verify that messages can be correctly encrypted and decrypted using the generated keys.

## Additional Features

- **Send Files**

   To send a file, use the following command:

   ```bash
   /sendfile {File_Path}
   ```

## Notes

- Ensure that the server and clients use the correct keys for message encryption and decryption.
- By default, messages are not encrypted during client-server communication. You can extend the code to integrate RSA encryption into the message transmission.

## License

This project is open-source and available under the MIT License. Feel free to modify and enhance the code.

## Contributions

Contributions are welcome! If you would like to improve the project, feel free to open an issue or submit a pull
