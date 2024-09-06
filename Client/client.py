import socket
import threading
import sys
import os
from colorama import Fore
import colorama

def client():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)  # Establece un tiempo de espera para la conexión
    try:
        client_socket.connect((host, 5555))
        client_socket.send(nickname.encode('utf-8'))

        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        write_thread = threading.Thread(target=write)
        write_thread.start()

    except socket.error as e:
        print(Fore.RED + f"Socket error: {e}")
        sys.exit()

def print_help():
    help_text = """
    Available commands:
    /sendfile <file_path>  - Send a file to the chat.
    /exit                  - Exit the chat.
    /help                  - Show this help message.
    """
    print(Fore.YELLOW + help_text)

def receive():
    while True:
        try:
            header = client_socket.recv(1024).decode('utf-8')
            if not header:  # Si no hay más datos, se asume que la conexión se ha cerrado
                break
            if header.startswith('FILE'):
                _, filename, file_size = header.split(':')
                file_size = int(file_size)
                print(Fore.BLUE + f"Receiving file: {filename} ({file_size} bytes)")
                
                with open(f"received_{filename}", "wb") as f:
                    while file_size > 0:
                        data = client_socket.recv(min(file_size, 4096))
                        if not data:
                            break
                        f.write(data)
                        file_size -= len(data)
                
                print(Fore.GREEN + f"File {filename} received successfully!")
            else:
                print(Fore.CYAN + header)
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            break
    client_socket.close()

def write():
    print_help()
    while True:
        try:
            message = input(f'{nickname}: ')
            if message.startswith("/sendfile"):
                _, file_path = message.split(' ', 1)
                send_file(file_path)
            elif message == "/help":
                print_help()
            elif message == "/exit":
                print(Fore.RED + "Exiting chat...")
                client_socket.close()
                break
            else:
                client_socket.send(f"{nickname}: {message}".encode('utf-8'))
        except Exception as e:
            print(Fore.RED + f"An error occurred while sending: {e}")
            break

def send_file(file_path):
    try:
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        client_socket.send(f"FILE:{filename}:{file_size}".encode('utf-8'))
        print(Fore.YELLOW + f"Sending file: {filename} ({file_size} bytes)")

        with open(file_path, "rb") as f:
            while (data := f.read(4096)):
                client_socket.send(data)
        
        print(Fore.GREEN + f"File {filename} sent successfully!")
    except FileNotFoundError:
        print(Fore.RED + f"File {file_path} not found.")
    except Exception as e:
        print(Fore.RED + f"Failed to send file {file_path}: {e}")

def main():
    colorama.init(autoreset=True)
    global nickname
    global host
    global client_socket

    host = input(Fore.GREEN + "\nEnter the server's IP: ")
    nickname = input(Fore.GREEN + "\nPlease enter your nickname: ")

    client()

if __name__ == "__main__":
    main()
