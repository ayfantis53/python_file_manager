"""Server for recieving messages."""

# Standard lib imports
import socket


# ================
# Global variables.
# ================
HOST = "localhost"
PORT = 9090


# creates new socket object for reliable, connection-oriented TCP communication over IPv4.
# assigns a specific network interface (IP address) and a port number to a socket instance.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

# prepares a server socket to accept incoming network connections by enabling "passive" server mode.
server.listen()

# Used by a network server to accept an incoming connection request from a client.
communication_socket, address = server.accept()

# Control flow statement used to create an infinite loop.
while True:
    print(f"Server Connected to {address}")

    # reads up to 1024 bytes of incoming data from a connected client and decodes it into a standard
    # Python string. It is used for handling incoming messages in TCP networking.
    message = communication_socket.recv(1024).decode("utf-8")
    print(f"Message from client is {message}")

    # Converts the string into a bytes object & transmits it over the network via a socket connection.
    communication_socket.send("Server Got your message! Thank you".encode("utf-8"))
    print(f"Communication with {address} ended!")
