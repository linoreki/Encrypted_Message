import socket
import threading
import os
import customtkinter as ctk
from tkinter import scrolledtext, filedialog, messagebox

port = 5555

def connect_to_server():
    global nickname
    global host
    nickname = nickname_entry.get()
    host = host_entry.get()
    if nickname and host:
        client.connect((host, port))
        connect_window.destroy()
        start_chat()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive():
    while True:
        try:
            header = client.recv(1024).decode('utf-8')
            if header.startswith('FILE'):
                _, filename, file_size = header.split(':')
                file_size = int(file_size)
                chat_area.config(state="normal")
                chat_area.insert("end", f"Receiving file: {filename} ({file_size} bytes)\n", 'blue')
                chat_area.config(state="disabled")

                with open(f"received_{filename}", "wb") as f:
                    while file_size > 0:
                        data = client.recv(min(file_size, 4096))
                        f.write(data)
                        file_size -= len(data)
                
                chat_area.config(state="normal")
                chat_area.insert("end", f"File {filename} received successfully!\n", 'green')
                chat_area.config(state="disabled")
            else:
                chat_area.config(state="normal")
                chat_area.insert("end", header + '\n', 'cyan')
                chat_area.config(state="disabled")
        except Exception as e:
            chat_area.config(state="normal")
            chat_area.insert("end", f"An error occurred: {e}\n", 'red')
            chat_area.config(state="disabled")
            client.close()
            break

def send_message(event=None):
    message = message_entry.get()
    message_entry.delete(0, "end")
    if message:
        if message.startswith("/sendfile"):
            _, file_path = message.split(' ', 1)
            send_file(file_path)
        elif message == "/exit":
            chat_area.config(state="normal")
            chat_area.insert("end", "Exiting chat...\n", 'red')
            chat_area.config(state="disabled")
            client.close()
            app.quit()
        else:
            client.send(f"{nickname}: {message}".encode('utf-8'))

def send_file(file_path=None):
    if not file_path:
        file_path = filedialog.askopenfilename()
    if not file_path:
        return

    try:
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        
        client.send(f"FILE:{filename}:{file_size}".encode('utf-8'))
        
        chat_area.config(state="normal")
        chat_area.insert("end", f"Sending file: {filename} ({file_size} bytes)\n", 'yellow')
        chat_area.config(state="disabled")

        with open(file_path, "rb") as f:
            while (data := f.read(4096)):
                client.send(data)
        
        chat_area.config(state="normal")
        chat_area.insert("end", f"File {filename} sent successfully!\n", 'green')
        chat_area.config(state="disabled")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file_path} not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send file {file_path}: {e}")

def start_chat():
    global app, chat_area, message_entry

    app = ctk.CTk()
    app.title("Encrypted Chat Client")
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    chat_frame = ctk.CTkFrame(app)
    chat_frame.pack(padx=10, pady=5, fill="both", expand=True)

    # Usamos scrolledtext de Tkinter aquí para el área de chat
    chat_area = scrolledtext.ScrolledText(chat_frame, wrap="word", height=20, width=50, bg="#1c1c1c", fg="#ffffff", insertbackground="#ffffff")
    chat_area.tag_configure('blue', foreground='lightblue')
    chat_area.tag_configure('green', foreground='lightgreen')
    chat_area.tag_configure('cyan', foreground='cyan')
    chat_area.tag_configure('yellow', foreground='yellow')
    chat_area.tag_configure('red', foreground='red')
    chat_area.config(state="disabled")
    chat_area.pack(side="left", fill="both", expand=True)

    message_frame = ctk.CTkFrame(app)
    message_frame.pack(padx=10, pady=5, fill="x")

    message_entry = ctk.CTkEntry(message_frame, width=380)
    message_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
    message_entry.bind("<Return>", send_message)

    send_button = ctk.CTkButton(message_frame, text="Send", command=send_message)
    send_button.pack(side="left", padx=5, pady=5)

    file_button = ctk.CTkButton(message_frame, text="Send File", command=send_file)
    file_button.pack(side="left", padx=5, pady=5)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    app.mainloop()

connect_window = ctk.CTk()
connect_window.title("Connect to Chat")

nickname_label = ctk.CTkLabel(connect_window, text="Enter your nickname:")
nickname_label.pack(padx=10, pady=5)

nickname_entry = ctk.CTkEntry(connect_window)
nickname_entry.pack(padx=10, pady=5)

host_label = ctk.CTkLabel(connect_window, text="Enter The Server IP")
host_label.pack(padx=10, pady=5)

host_entry = ctk.CTkEntry(connect_window)
host_entry.pack(padx=10, pady=5)

connect_button = ctk.CTkButton(connect_window, text="Connect", command=connect_to_server)
connect_button.pack(padx=10, pady=10)

connect_window.mainloop()
