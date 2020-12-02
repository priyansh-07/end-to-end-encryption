"""
Server side script
"""
import socket
import threading

connections = []
total_connections = 0

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(4096)
            except:
                print("Client " + str(self.address) + " has been disconnected.")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                print("[Client " + str(self.id) + "] " + str(data.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)

# wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("Client " + str(connections[len(connections) - 1]) + " is connected.")
        total_connections += 1

def main():
    print('SERVER RUNNING...')
    host = '127.0.0.1' # you may change host to your own IP address
    port = 5000 # you may change this port to your custom port as long as server and client are a match

    # create a socket service
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    # create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    print('SERVER LISTENING...')
    
if __name__ == '__main__':
    main()
