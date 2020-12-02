"""
Client Side Script
"""

# Sample code to check if the base project is working
from encryption import aes_256_encryption
e = aes_256_encryption()
#from encryption import aes_256_encryption
#e = aes_256_encryption()

import socket
import threading
import sys

def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(4096)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break

def main():
    host = '127.0.0.1' # you may change host to your own IP address
    port = 5000 # you may change this port to your custom port as long as server and client are a match

    # try to connect to the server app
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except:
        print("Connection failed. Cannot find server. Make sure host and port are the same.")
        sys.exit(0)

    # create new thread to wait for data
    receiveThread = threading.Thread(target = receive, args = (sock, True))
    receiveThread.start()

    while True:
        message = input()
        sock.sendall(str.encode(message))

if __name__ == '__main__':
    main()
