import socket
import threading

# Define the host and port to use
host = "localhost"
port = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {host}:{port}...")

# Define a function to handle a client connection
def handle_client(client_socket, client_address):
    print(f"Connected to {client_address}...")
    # Receive messages from the client and broadcast them to all other clients
    while True:
        try:
            # Receive the message from the client
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"{client_address}: {message}")
            # Broadcast the message to all other clients
            for socket in clients:
                if socket != client_socket:
                    socket.send(message.encode())
        except:
            break
    # Close the client socket
    client_socket.close()
    print(f"Disconnected from {client_address}...")

# Keep track of all client sockets
clients = []

# Accept incoming connections and create a thread to handle each one
while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()