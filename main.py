import threading
import queue
import customtkinter as ctk
from server import server
from client import client, clientGUI
import test
import gen_key

task_queue = queue.Queue()

def execute_option(option):
    try:
        if option == 'Server':
            server.main()
        elif option == 'Client':
            client.main()
        elif option == 'Client GUI':
            clientGUI.main()
        elif option == 'Test':
            test.main()
        elif option == 'Key Generation':
            gen_key.main()
        else:
            print("Invalid option.")
    except Exception as e:
        print(f"Error executing {option}: {e}")

def run_in_thread(option):
    thread = threading.Thread(target=execute_option, args=(option,))
    thread.start()

def check_queue():
    while not task_queue.empty():
        task = task_queue.get()
        print(task)
    app.after(100, check_queue) 
def main():
    global app

    app = ctk.CTk() 
    app.title("Main Menu")
    app.geometry("400x400")

    label = ctk.CTkLabel(app, text="Choose an option to execute", font=("Arial", 16))
    label.pack(pady=20)

    button_server = ctk.CTkButton(app, text="Server", command=lambda: run_in_thread('Server'))
    button_server.pack(pady=10)

    button_client = ctk.CTkButton(app, text="Client", command=lambda: run_in_thread('Client'))
    button_client.pack(pady=10)

    button_gui = ctk.CTkButton(app, text="Client GUI", command=lambda: run_in_thread('Client GUI'))
    button_gui.pack(pady=10)

    button_test = ctk.CTkButton(app, text="Test", command=lambda: run_in_thread('Test'))
    button_test.pack(pady=10)

    button_keygen = ctk.CTkButton(app, text="Key Generation", command=lambda: run_in_thread('Key Generation'))
    button_keygen.pack(pady=10)

    app.after(100, check_queue)

    app.mainloop()

if __name__ == "__main__":
    main()
