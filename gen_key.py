# gen_key.py
from Crypto.PublicKey import RSA

def generate_rsa_keys():
    key = RSA.generate(3072)
    return key

def save_key(key, file_path):
    with open(file_path, "wb") as key_file:
        key_file.write(key.export_key())

def main():
    # Generate server keys
    server_key = generate_rsa_keys()
    save_key(server_key, "server/key_private.pem")
    save_key(server_key.public_key(), "server/key_public.pem")

    # Generate client keys
    client_key = generate_rsa_keys()
    save_key(client_key, "client/key_private.pem")
    save_key(client_key.public_key(), "client/key_public.pem")

    print("Keys generated and saved successfully.")

if __name__ == "__main__":
    main()
