# server/add_key.py

def add_key(public_key_path, allowed_keys_path):
    try:
        with open(public_key_path, "r") as key_file:
            public_key = key_file.read().strip()

        # Ensure the key starts with BEGIN PUBLIC KEY and ends with END PUBLIC KEY
        if '-----BEGIN PUBLIC KEY-----' not in public_key or '-----END PUBLIC KEY-----' not in public_key:
            print("Invalid public key format.")
            return

        # Extract the part between BEGIN and END lines, and ensure there are no duplicates
        start_index = public_key.index('-----BEGIN PUBLIC KEY-----')
        end_index = public_key.index('-----END PUBLIC KEY-----') + len('-----END PUBLIC KEY-----')
        cleaned_key = public_key[start_index:end_index].strip()
        print(cleaned_key)
        # Open allowed_keys.txt in append mode
        with open(allowed_keys_path, "a") as allowed_keys_file:
            allowed_keys_file.write(cleaned_key + '\n\n')  # Ensure there's a newline after each key

        print("Key added successfully.")
    except Exception as e:
        print(f"Error adding key: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python add_key.py <public_key_path> <allowed_keys_path>")
    else:
        add_key(sys.argv[1], sys.argv[2])
