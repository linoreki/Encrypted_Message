import socket
import threading
import tkinter as tk
import customtkinter as ctk

def main():
    host = '0.0.0.0'
    port = 5555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    clients = []
    nicknames = {}
    banned_ips = set()
    banned_nicknames = set()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Server Management")
    app.geometry("900x600")

    main_frame = ctk.CTkFrame(app, corner_radius=10)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    title_label = ctk.CTkLabel(main_frame, text="Server Management Console", font=("Arial", 26, "bold"))
    title_label.pack(pady=10)

    # Reorganizar para que el chat ocupe más espacio
    messages_frame = ctk.CTkFrame(main_frame, corner_radius=10)
    messages_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

    messages_label = ctk.CTkLabel(messages_frame, text="Messages", font=("Arial", 18))
    messages_label.pack(pady=10)
    messages_textbox = ctk.CTkTextbox(messages_frame, width=50, height=10, state="disabled", font=("Arial", 14))
    messages_textbox.pack(padx=10, pady=10, fill="both", expand=True)

    # Marco para clientes y controles
    side_frame = ctk.CTkFrame(main_frame, corner_radius=10)
    side_frame.pack(side="left", padx=10, pady=10, fill="y")

    clients_label = ctk.CTkLabel(side_frame, text="Connected Clients", font=("Arial", 18))
    clients_label.pack(pady=10)
    clients_listbox = tk.Listbox(side_frame, width=25, height=10, bg="#2C2F33", fg="white", bd=0, highlightthickness=0, font=("Arial", 14))
    clients_listbox.pack(padx=10, pady=10)

    # Controles
    control_frame = ctk.CTkFrame(side_frame, corner_radius=10)
    control_frame.pack(pady=10)

    kick_button = ctk.CTkButton(control_frame, text="Kick User", command=lambda: kick_user(), font=("Arial", 14))
    kick_button.grid(row=0, column=0, padx=10, pady=10)

    ban_button = ctk.CTkButton(control_frame, text="Ban User", command=lambda: ban_user(), font=("Arial", 14))
    ban_button.grid(row=0, column=1, padx=10, pady=10)

    unban_button = ctk.CTkButton(control_frame, text="Unban User", command=lambda: unban_user(), font=("Arial", 14))
    unban_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    view_banned_button = ctk.CTkButton(control_frame, text="View Banned Users", command=lambda: view_banned(), font=("Arial", 14))
    view_banned_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def update_client_list():
        clients_listbox.delete(0, tk.END)
        for nickname in nicknames.values():
            clients_listbox.insert(tk.END, nickname)

    def broadcast(message, sender_socket=None):
        for client in clients:
            if client != sender_socket:
                client.send(message)

    def handle_client(client_socket, client_address):
        ip_address = client_address[0]
        
        if ip_address in banned_ips:
            client_socket.send(b"Your IP is banned from this server.")
            client_socket.close()
            return

        nickname = client_socket.recv(256).decode('utf-8')
        
        if nickname in banned_nicknames:
            client_socket.send(b"Your nickname is banned from this server.")
            client_socket.close()
            return

        print(f"Connected with {client_address}")
        clients.append(client_socket)
        nicknames[client_socket] = nickname
        update_client_list()

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
                    messages_textbox.configure(state="normal")
                    messages_textbox.insert(tk.END, f"File {filename} received.\n")
                    messages_textbox.configure(state="disabled")
                else:
                    broadcast(message)
                    messages_textbox.configure(state="normal")
                    messages_textbox.insert(tk.END, f"{nickname}: {message.decode('utf-8')}\n")
                    messages_textbox.configure(state="disabled")
            except:
                clients.remove(client_socket)
                client_socket.close()
                nickname = nicknames.pop(client_socket, "Unknown")
                update_client_list()
                print(f"{nickname} disconnected")
                messages_textbox.configure(state="normal")
                messages_textbox.insert(tk.END, f"{nickname} disconnected.\n")
                messages_textbox.configure(state="disabled")
                break

    def receive():
        while True:
            client_socket, client_address = server.accept()
            handle_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            handle_thread.start()

    def kick_user():
        selected = clients_listbox.curselection()
        if selected:
            selected_nickname = clients_listbox.get(selected)
            for client_socket, nickname in nicknames.items():
                if nickname == selected_nickname:
                    client_socket.send(b"KICK")
                    client_socket.close()
                    clients.remove(client_socket)
                    nicknames.pop(client_socket)
                    update_client_list()
                    messages_textbox.configure(state="normal")
                    messages_textbox.insert(tk.END, f"{selected_nickname} was kicked.\n")
                    messages_textbox.configure(state="disabled")
                    break

    def ban_user():
        selected = clients_listbox.curselection()
        if selected:
            selected_nickname = clients_listbox.get(selected)
            for client_socket, nickname in nicknames.items():
                if nickname == selected_nickname:
                    ip_address = client_socket.getpeername()[0]
                    banned_ips.add(ip_address)
                    banned_nicknames.add(nickname)
                    client_socket.send(b"BAN")
                    client_socket.close()
                    clients.remove(client_socket)
                    nicknames.pop(client_socket)
                    update_client_list()
                    messages_textbox.configure(state="normal")
                    messages_textbox.insert(tk.END, f"{selected_nickname} was banned.\n")
                    messages_textbox.configure(state="disabled")
                    break

    def unban_user():
        identifier = tk.simpledialog.askstring("Unban User", "Enter IP or Nickname to unban:")
        if identifier:
            if identifier in banned_ips:
                banned_ips.remove(identifier)
                messages_textbox.configure(state="normal")
                messages_textbox.insert(tk.END, f"IP {identifier} was unbanned.\n")
                messages_textbox.configure(state="disabled")
            elif identifier in banned_nicknames:
                banned_nicknames.remove(identifier)
                messages_textbox.configure(state="normal")
                messages_textbox.insert(tk.END, f"Nickname {identifier} was unbanned.\n")
                messages_textbox.configure(state="disabled")
            else:
                messages_textbox.configure(state="normal")
                messages_textbox.insert(tk.END, f"{identifier} not found in ban list.\n")
                messages_textbox.configure(state="disabled")

    def view_banned():
        banned_users_window = ctk.CTkToplevel(app)
        banned_users_window.title("Banned Users")
        banned_users_window.geometry("400x300")

        banned_label = ctk.CTkLabel(banned_users_window, text="Banned Users", font=("Arial", 18))
        banned_label.pack(pady=10)

        banned_textbox = ctk.CTkTextbox(banned_users_window, state="disabled", font=("Arial", 14))
        banned_textbox.pack(padx=10, pady=10, fill="both", expand=True)

        banned_textbox.configure(state="normal")
        if banned_ips or banned_nicknames:
            banned_textbox.insert(tk.END, "Banned IPs:\n")
            for ip in banned_ips:
                banned_textbox.insert(tk.END, f"{ip}\n")
            banned_textbox.insert(tk.END, "\nBanned Nicknames:\n")
            for nickname in banned_nicknames:
                banned_textbox.insert(tk.END, f"{nickname}\n")
        else:
            banned_textbox.insert(tk.END, "No users are currently banned.\n")
        banned_textbox.configure(state="disabled")

    threading.Thread(target=receive).start()

    print("Server is listening...")
    app.mainloop()

if __name__ == "__main__":
    main()
