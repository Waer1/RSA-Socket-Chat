import socket
import base64
import sys
import threading
import json
from RSA import Encrypt, Decrypt, generate_two_distinct_primes, generate_keypair
sys.setrecursionlimit(1500)

# Create a socket object for the client
client_socket = socket.socket()

# Get local machine name
host = socket.gethostname()

# Reserve a port for your service.
port = 12345

# Connect to the server
client_socket.connect((host, port))

# Generate the public and private keys for the client
p , q = generate_two_distinct_primes()
public_key, private_key = generate_keypair(p, q)

# Send the public key to the server
# public_key_str = base64.b64encode(str(public_key).encode('utf-8')).decode('utf-8')
# client_socket.send(public_key_str.encode('utf-8'))

public_key_str = json.dumps(public_key)
public_key_str_encoded = base64.b64encode(public_key_str.encode('utf-8'))
client_socket.send(public_key_str_encoded)

# Receive the other client's public key from the server
other_public_key_str = client_socket.recv(1024).decode('utf-8')
other_public_key = eval(base64.b64decode(other_public_key_str.encode('utf-8')).decode('utf-8'))
print('Received public key of other client:', other_public_key)

# Send the client's name to the server
name = input('Enter your name: ')
client_socket.send(name.encode('utf-8'))

# Receive the other client's name from the server
other_name = client_socket.recv(1024).decode('utf-8')
print('Other client name:', other_name)

# Start the chat
print('Starting chat...')
def receive_message():
    while True:
        # Send a message to the other client
        message = input('> ')
        # Encrypt message using other_public_key
        encrypted_message = Encrypt(message, other_public_key)
        # Send encrypted message to other client
        encrypted_message_send = base64.b64encode(encrypted_message.to_bytes((encrypted_message.bit_length() + 7) // 8, 'big')).decode('utf-8')
        # print("the cipher text is : ",encrypted_message_send)
        client_socket.send(encrypted_message_send.encode('utf-8'))    


receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

while True:
    # Receive a message from the other client
    encrypted_message = client_socket.recv(1024).decode('utf-8')
    # print("the cipher text is : ",encrypted_message)
    encrypted_int = int.from_bytes(base64.b64decode(encrypted_message.encode('utf-8')), byteorder='big')
    decrypted_message = Decrypt(encrypted_int, private_key)
    print(other_name + ': ' + decrypted_message)

# Close the connection
client_socket.close()