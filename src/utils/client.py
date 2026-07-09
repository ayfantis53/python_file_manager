"""Imitates Client Sending message."""

# Standard lib imports
import socket
import sys


# ================
# Global variables.
# ================
HOST = "localhost"
PORT = 8089
IS_PRIMARY = "isprimary"


# creates new socket object for reliable, connection-oriented TCP communication over IPv4.
# assigns a specific network interface (IP address) and a port number to a socket instance.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print(f"Connected to port {PORT}")

# There is an input.
if len(sys.argv) > 1:
    user_input = sys.argv[1]

    # is_primary is true.
    if user_input == "true" or user_input == "True":
        IS_PRIMARY = "isprimary"
    # is_primary is false.
    elif user_input == "false" or user_input == "False":
        IS_PRIMARY = "isNOTprimary"
# There is NO input.
else:
    IS_PRIMARY = "isprimary"

# Converts the string into a bytes object & transmits it over the network via a socket connection.
client.send(IS_PRIMARY.encode("utf-8"))
print(client.recv(1024).decode("utf-8"))
