# RSA-Socket-Chat

This is a simple chat application that uses RSA encryption to secure communication between clients. The application generates RSA keys automatically for each client, and the public key is exchanged at the beginning of the conversation to allow for secure encryption and decryption of messages.

## Installation

1. Clone the repository: `git clone https://github.com/yourusername/RSA-Socket-Chat.git`
2. Navigate to the project directory: `cd RSA-Socket-Chat`
3. Install the required packages: `pip install -r requirements.txt`

## Usage

To start the chat application, run the following command in your terminal:
- python Application/server.py
- python Application/client.py
- wait for second 
- python Application/client.py
- type name1
- type name2
- start texting


This will start the server and two clients in separate terminal windows. The clients will automatically generate RSA keys for encryption and decryption, and exchange their public keys at the beginning of the conversation to allow for secure communication.

To start chatting, enter your name when prompted and start sending messages to the other client.

