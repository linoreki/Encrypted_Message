import socket
import threading
import sys
import os
import time
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

host = '172.0.0.1'
nickname = input(Fore.GREEN + "\nPlease enter your nickname: ")

if len(sys.argv) == 2:
    host = sys.argv[1]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, 5555))

def print_help():
    help_text = """
    Available commands:
    /sendfile <file_path>  - Send a file to the chat (max 10MB).
    /exit                  - Exit the chat.
    /help                  - Show this help message.
    """
    print(Fore.YELLOW + help_text)

def receive():
    while True:
        try:
            header = client.recv(1024).decode('utf-8')
            if header.startswith('FILE'):
                _, filename, file_size = header.split(':')
                file_size = int(file_size)
                print(Fore.BLUE + f"Receiving file: {filename} ({file_size} bytes)")
                with open(f"received_{filename}", "wb") as f:
                    while file_size > 0:
                        data = client.recv(min(file_size, 4096))
                        f.write(data)
                        file_size -= len(data)
                print(Fore.GREEN + f"File {filename} received successfully!")
            else:
                print(Fore.CYAN + header)
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            client.close()
            break

def write():
    print_help()
    while True:
        message = input(f'{nickname}: ')
        if message.startswith("/sendfile"):
            _, file_path = message.split(' ', 1)
            send_file(file_path)
        elif message == "/help":
            print_help()
        elif message == "/exit":
            print(Fore.RED + "Exiting chat...")
            client.close()
            break
        else:
            client.send(f"{nickname}: {message}".encode('utf-8'))

def send_file(file_path):
    try:
        file_size = os.path.getsize(file_path)
        if file_size > 4 * 1024:  # 4kb limit
            print(Fore.RED + "File size exceeds the 4kb limit.")
            return

        filename = os.path.basename(file_path)
        client.send(f"FILE:{filename}:{file_size}".encode('utf-8'))
        print(Fore.YELLOW + f"Sending file: {filename} ({file_size} bytes)")

        with open(file_path, "rb") as f:
            while (data := f.read(4096)):
                client.send(data)
        print(Fore.GREEN + f"File {filename} sent successfully!")
    except FileNotFoundError:
        print(Fore.RED + f"File {file_path} not found.")
    except Exception as e:
        print(Fore.RED + f"Failed to send file {file_path}: {e}")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
