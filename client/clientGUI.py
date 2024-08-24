import socket
import threading
import sys
import os
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox

# Definición del host y puerto
port = 5555

# Función para iniciar sesión con un apodo
def connect_to_server():
    global nickname
    global host
    nickname = nickname_entry.get()
    host = host_entry.get()
    if nickname and host:
        client.connect((host, port))
        connect_window.destroy()
        start_chat()

# Conectar el cliente al servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Función para recibir mensajes
def receive():
    while True:
        try:
            header = client.recv(1024).decode('utf-8')
            if header.startswith('FILE'):
                _, filename, file_size = header.split(':')
                file_size = int(file_size)
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, f"Receiving file: {filename} ({file_size} bytes)\n", 'blue')
                chat_area.config(state=tk.DISABLED)

                with open(f"received_{filename}", "wb") as f:
                    while file_size > 0:
                        data = client.recv(min(file_size, 4096))
                        f.write(data)
                        file_size -= len(data)
                
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, f"File {filename} received successfully!\n", 'green')
                chat_area.config(state=tk.DISABLED)
            else:
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, header + '\n', 'cyan')
                chat_area.config(state=tk.DISABLED)
        except Exception as e:
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, f"An error occurred: {e}\n", 'red')
            chat_area.config(state=tk.DISABLED)
            client.close()
            break

# Función para enviar mensajes
def send_message(event=None):
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    if message:
        if message.startswith("/sendfile"):
            _, file_path = message.split(' ', 1)
            send_file(file_path)
        elif message == "/exit":
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, "Exiting chat...\n", 'red')
            chat_area.config(state=tk.DISABLED)
            client.close()
            app.quit()
        else:
            client.send(f"{nickname}: {message}".encode('utf-8'))

# Función para enviar archivos
def send_file(file_path=None):
    if not file_path:
        file_path = filedialog.askopenfilename()
    if not file_path:
        return

    try:
        file_size = os.path.getsize(file_path)
        if file_size > 4 * 1024:  # 4kb limit
            messagebox.showerror("Error", "File size exceeds the 4kb limit.")
            return

        filename = os.path.basename(file_path)
        client.send(f"FILE:{filename}:{file_size}".encode('utf-8'))
        
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f"Sending file: {filename} ({file_size} bytes)\n", 'yellow')
        chat_area.config(state=tk.DISABLED)

        with open(file_path, "rb") as f:
            while (data := f.read(4096)):
                client.send(data)
        
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f"File {filename} sent successfully!\n", 'green')
        chat_area.config(state=tk.DISABLED)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file_path} not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send file {file_path}: {e}")

# Función para iniciar la ventana de chat
def start_chat():
    global app, chat_area, message_entry

    app = tk.Tk()
    app.title("Encrypted Chat Client")
    
    # Colores del tema oscuro
    bg_color = "#1c1c1c"        # Fondo oscuro
    fg_color = "#ffffff"        # Texto claro
    entry_bg_color = "#333333"  # Fondo de entradas
    button_bg_color = "#444444" # Fondo de botones
    button_fg_color = "#ffffff" # Texto de botones

    app.configure(bg=bg_color)

    chat_frame = tk.Frame(app, bg=bg_color)
    chat_frame.pack(padx=10, pady=5)

    chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, height=20, width=50, bg=bg_color, fg=fg_color, insertbackground=fg_color)
    chat_area.tag_config('blue', foreground='lightblue')
    chat_area.tag_config('green', foreground='lightgreen')
    chat_area.tag_config('cyan', foreground='cyan')
    chat_area.tag_config('yellow', foreground='yellow')
    chat_area.tag_config('red', foreground='red')
    chat_area.config(state=tk.DISABLED)
    chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    message_frame = tk.Frame(app, bg=bg_color)
    message_frame.pack(padx=10, pady=5)

    message_entry = tk.Entry(message_frame, width=40, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
    message_entry.pack(side=tk.LEFT, padx=5, pady=5)
    message_entry.bind("<Return>", send_message)

    send_button = tk.Button(message_frame, text="Send", command=send_message, bg=button_bg_color, fg=button_fg_color)
    send_button.pack(side=tk.LEFT, padx=5, pady=5)

    file_button = tk.Button(message_frame, text="Send File", command=send_file, bg=button_bg_color, fg=button_fg_color)
    file_button.pack(side=tk.LEFT, padx=5, pady=5)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    app.mainloop()

# Ventana para ingresar el nickname y la ip
connect_window = tk.Tk()
connect_window.title("Connect to Chat")

# Configuración del tema oscuro
bg_color = "#1c1c1c"        # Fondo oscuro
fg_color = "#ffffff"        # Texto claro
entry_bg_color = "#333333"  # Fondo de entradas
button_bg_color = "#444444" # Fondo de botones
button_fg_color = "#ffffff" # Texto de botones

connect_window.configure(bg=bg_color)

nickname_label = tk.Label(connect_window, text="Enter your nickname:", bg=bg_color, fg=fg_color)
nickname_label.pack(padx=10, pady=5)

nickname_entry = tk.Entry(connect_window, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
nickname_entry.pack(padx=10, pady=5)

host_label = tk.Label(connect_window, text="Enter The Server IP", bg=bg_color, fg=fg_color)
host_label.pack(padx=10, pady=5)

host_entry = tk.Entry(connect_window, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
host_entry.pack(padx=10, pady=5)

connect_button = tk.Button(connect_window, text="Connect", command=connect_to_server, bg=button_bg_color, fg=button_fg_color)
connect_button.pack(padx=10, pady=10)


connect_window.mainloop()

