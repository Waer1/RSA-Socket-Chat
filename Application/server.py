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

# Dictionary to store client names
client_names = {}
# Dictionary to store client Keys
client_keys = {}


# Define a function to handle a client connection
def handle_client(client_socket, client_address):
    print(f"Connected to {client_address}...")
    # Receive the client's name
    client_name = client_socket.recv(1024).decode()
    # Store the client's name in the dictionary
    client_names[client_socket] = client_name

    
    # Send a welcome message to the client
    welcome_message = f"Welcome to the chat, {client_name}!"
    client_socket.send(welcome_message.encode())
    # Receive messages from the client and broadcast them to all other clients
    while True:
        try:
            # Receive the message from the client
            message = client_socket.recv(1024).decode()
            if not message:
                break
            # Prepend the client's name to the message
            message_with_name = f"{client_names[client_socket]}: {message}"
            print(message_with_name)
            # Broadcast the message to all other clients
            for socket in client_names:
                if socket != client_socket:
                    socket.send(message_with_name.encode())
        except:
            break
    # Remove the client's name from the dictionary
    del client_names[client_socket]
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