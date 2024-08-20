import socket
import threading
import sys

host = '127.0.0.1'
nickname = input("\nPlease enter your nickname: ")

if len(sys.argv) == 2:
    host = sys.argv[1]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, 5555))

def receive():
    while True:
        try:
            message = client.recv(256)
            print(message.decode('utf-8'))
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

def write():
    while True:
        message = input('You: ')
        client.send(f"{nickname}: {message}".encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
