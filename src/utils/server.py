import socket

HOST = 'localhost'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

communication_socket, address = server.accept()

while True:
    print(f"Connected to {address}")

    message = communication_socket.recv(1024).decode('utf-8')
    print(f"Message from client is {message}")

    communication_socket.send(f"HSD Got your message! Thank you". encode('utf-8'))
    print(f"Communcation with {address} ended!")

    # communication_socket.close()