import socket
import threading

# Server Settings
host = '0.0.0.0'
port = 5555

# Start Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []

# Broadcast Messages to All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle Individual Client Connections
def handle_client(client_socket, client_address):
    print(f"Connected with {client_address}")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(256)
            broadcast(f"{client_address[0]}: {message.decode('utf-8')}".encode('utf-8'))
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

# Main Receive Loop
def receive():
    while True:
        client_socket, client_address = server.accept()
        handle_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        handle_thread.start()

print("Server is listening...")
receive()
