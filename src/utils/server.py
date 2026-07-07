"""Server for recieving messages."""

# Standard lib imports
import socket


# ================
# Global variables.
# ================
HOST = "localhost"
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

communication_socket, address = server.accept()

while True:
    print(f"Server Connected to {address}")

    message = communication_socket.recv(1024).decode("utf-8")
    print(f"Message from client is {message}")

    communication_socket.send("HSD Got your message! Thank you".encode("utf-8"))
    print(f"Communication with {address} ended!")

    # communication_socket.close()
