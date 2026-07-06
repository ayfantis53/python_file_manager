# IMITATES HSD SENDING MESSAGE
import socket

HOST = 'localhost'
PORT = 8089

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print(f"Connected to port {PORT}")

client.send("isprimary".encode('utf-8'))
print(client.recv(1024).decode('utf-8'))