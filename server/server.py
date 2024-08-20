import socket
import threading

host = '0.0.0.0'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = {}

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:  
            client.send(message)

def handle_client(client_socket, client_address):
    print(f"Connected with {client_address}")
    clients.append(client_socket)

    nickname = client_socket.recv(256).decode('utf-8')
    nicknames[client_socket] = nickname

    while True:
        try:
            message = client_socket.recv(4096)
            if message.startswith(b'FILE'):
                _, filename, file_size = message.decode('utf-8').split(':')
                file_size = int(file_size)
                broadcast(message, client_socket)
                while file_size > 0:
                    data = client_socket.recv(4096)
                    broadcast(data, client_socket)
                    file_size -= len(data)
                print(f"File {filename} received and broadcasted.")
            else:
                broadcast(message)
        except:
            clients.remove(client_socket)
            client_socket.close()
            nickname = nicknames.pop(client_socket, "Unknown")
            print(f"{nickname} disconnected")
            break

def receive():
    while True:
        client_socket, client_address = server.accept()
        handle_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        handle_thread.start()

print("Server is listening...")
receive()
