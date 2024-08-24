import sys
import os
from server import server
from client import client, clientGUI
import test
import gen_key

def main():
    if len(sys.argv) != 2:
        print("Usage: main.py -s | -c | -g | -t | -l")
        sys.exit(1)

    option = sys.argv[1]

    print(option)

    if option == '-s':
        server.main()
    elif option == '-c':
        client.main()
    elif option == '-g':
        clientGUI.main()
    elif option == '-t':
        test.main()
    elif option == '-k':
        gen_key.main()
    else:
        print("Invalid option. Use -s for server, -c for client, -g for client GUI, -t for test, or -l for key generation.")
        sys.exit(1)

if __name__ == "__main__":
    main()
