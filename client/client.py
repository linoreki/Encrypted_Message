import socket
import threading
import sys

host = '127.0.0.1'
if len(sys.argv) == 2:
    host = sys.argv[1]
# Connect to Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

# Listening to Server
def receive():
    while True:
        try:
            message = client.recv(256)
            print(message.decode('utf-8'))
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

# Sending Messages to Server
def write():
    while True:
        message = input('')
        client.send(message.encode('utf-8'))

# Start Threads for Listening and Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
