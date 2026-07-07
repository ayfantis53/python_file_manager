"""Imitates HSD Sending message."""

# Standard lib imports
import socket
import sys


# ================
# Global variables.
# ================
HOST = "localhost"
PORT = 8089
IS_PRIMARY = "isprimary"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print(f"Connected to port {PORT}")

# Check for input
if len(sys.argv) > 1:
    user_input = sys.argv[1]
    if user_input == "true" or user_input == "True":
        IS_PRIMARY = "isprimary"
    elif user_input == "false" or user_input == "False":
        IS_PRIMARY = "isNOTprimary"
else:
    IS_PRIMARY = "isprimary"

client.send(IS_PRIMARY.encode("utf-8"))
print(client.recv(1024).decode("utf-8"))
