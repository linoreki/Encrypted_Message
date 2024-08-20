import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def load_key(file_path):
    """Load an RSA key from a PEM file."""
    try:
        with open(file_path, "rb") as key_file:
            return RSA.import_key(key_file.read())
    except Exception as e:
        print(f"Failed to load key from {file_path}: {e}")
        exit(1)

def test_encryption_decryption(public_key, private_key, message):
    """Test RSA encryption and decryption."""
    try:
        # Encrypt the message using the public key
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_message = cipher.encrypt(message.encode('utf-8'))
        print(f"Encrypted message: {base64.b64encode(encrypted_message).decode('utf-8')}")
        
        # Decrypt the message using the private key
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_message = cipher.decrypt(encrypted_message).decode('utf-8')
        print(f"Decrypted message: {decrypted_message}")
        
        # Check if the decrypted message matches the original message
        if decrypted_message == message:
            print("Encryption/Decryption successful!")
        else:
            print("Encryption/Decryption failed. Messages do not match.")
    except Exception as e:
        print(f"An error occurred during encryption/decryption: {e}")

def main():
    # Load server keys
    server_public_key = load_key("server/key_public.pem")
    server_private_key = load_key("server/key_private.pem")

    # Load client keys
    client_public_key = load_key("client/key_public.pem")
    client_private_key = load_key("client/key_private.pem")

    # Test server encryption/decryption
    print("\nTesting server key pair:")
    test_encryption_decryption(server_public_key, server_private_key, "Test message for server")

    # Test client encryption/decryption
    print("\nTesting client key pair:")
    test_encryption_decryption(client_public_key, client_private_key, "Test message for client")

if __name__ == "__main__":
    main()
