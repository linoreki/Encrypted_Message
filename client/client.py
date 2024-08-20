import socket
import threading
import sys
import os

host = '192.168.8.22'
nickname = input("\nPlease enter your nickname: ")

if len(sys.argv) == 2:
    host = sys.argv[1]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, 5555))

def receive():
    while True:
        try:
            message = client.recv(4096)
            if message.startswith(b'FILE'):
                _, filename, file_size = message.decode('utf-8').split(':')
                file_size = int(file_size)
                with open(f"received_{filename}", "wb") as f:
                    while file_size > 0:
                        data = client.recv(4096)
                        f.write(data)
                        file_size -= len(data)
                print(f"File {filename} received successfully!")
            else:
                print(message.decode('utf-8'))
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

def write():
    while True:
        message = input(f'You: ')
        if message.startswith("/sendfile"):
            _, file_path = message.split(' ', 1)
            send_file(file_path)
        else:
            client.send(f"{nickname}: {message}".encode('utf-8'))

def send_file(file_path):
    try:
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        client.send(f"FILE:{filename}:{file_size}".encode('utf-8'))
        with open(file_path, "rb") as f:
            while (data := f.read(4096)):
                client.send(data)
        print(f"File {filename} sent successfully!")
    except Exception as e:
        print(f"Failed to send file {file_path}: {e}")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
