import socket
import json
import base64
import threading

# Create a socket object
server_socket = socket.socket()

# Get local machine name
host = socket.gethostname()

# Reserve a port for your service.
port = 12345

# Bind the socket to the host and port
server_socket.bind((host, port))

# Wait for two clients to connect
print('Waiting for two connections...')
server_socket.listen(2)

# Accept the connections and receive the public keys
(client1_socket, client1_address) = server_socket.accept()
client1_public_key_encoded = client1_socket.recv(1024)
client1_public_key_json = base64.b64decode(client1_public_key_encoded).decode('utf-8')
client1_public_key = json.loads(client1_public_key_json)

print('Received public key from client 1:', client1_public_key)

(client2_socket, client2_address) = server_socket.accept()
client2_public_key_encoded = client2_socket.recv(1024)
client2_public_key_json = base64.b64decode(client2_public_key_encoded).decode('utf-8')
client2_public_key = json.loads(client2_public_key_json)
print('Received public key from client 2:', client2_public_key)



# Send each client the other's public key
client2_public_key_key_json = json.dumps(client2_public_key)
client2_public_key_key_encoded = base64.b64encode(client2_public_key_key_json.encode('utf-8'))
client1_socket.send(client2_public_key_key_encoded)


client1_public_key_key_json = json.dumps(client1_public_key)
client1_public_key_key_encoded = base64.b64encode(client1_public_key_key_json.encode('utf-8'))
client2_socket.send(client1_public_key_key_encoded)






# Receive the names from each client
client1_name = client1_socket.recv(1024).decode('utf-8')
print('Received name from client 1:', client1_name)

client2_name = client2_socket.recv(1024).decode('utf-8')
print('Received name from client 2:', client2_name)

# Send each client the other's name
client1_socket.send(client2_name.encode('utf-8'))
client2_socket.send(client1_name.encode('utf-8'))

# Start the chat
print('Starting chat...')
def receive_message():
    while True:
        # Receive a message from client 1 and send it to client 2
        client1_message = client1_socket.recv(1024).decode('utf-8')
        print(client1_name + ': ' + client1_message)
        client2_socket.send(client1_message.encode('utf-8'))

receive2_thread = threading.Thread(target=receive_message)
receive2_thread.start()

while True:
    # Receive a message from client 2 and send it to client 1
    client2_message = client2_socket.recv(1024).decode('utf-8')
    print(client2_name + 'aaa: ' + client2_message)
    client1_socket.send(client2_message.encode('utf-8'))

# Close the connections and the server socket
client1_socket.close()
client2_socket.close()
server_socket.close()
