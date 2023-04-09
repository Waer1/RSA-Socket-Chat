import socket
import threading

# Define the host and port to use
host = "localhost"
port = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))

print(f"Connected to server {host}:{port}...")

# Prompt the user to enter their name
user_name = input("Enter your name: ")
# Send the user's name to the server
client_socket.send(user_name.encode())

# Define a function to receive messages from the server
def receive_message():
    while True:
        # Receive the message from the server
        message = client_socket.recv(1024).decode()
        # Print the message to the console
        print(message)

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

# Send messages to the server
while True:
    # Prompt the user to enter a message
    message = input("")
    # Send the message to the server
    client_socket.send(message.encode())
