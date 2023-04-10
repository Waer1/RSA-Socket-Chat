#!/bin/bash

# Start the server in a new terminal window
gnome-terminal --title="Server" --command="python server.py"

# Wait for the server to start
sleep 5

# Start the first client in a new terminal window
gnome-terminal --title="Client 1" --command="python client.py"

# Start the second client in a new terminal window
gnome-terminal --title="Client 2" --command="python client.py"