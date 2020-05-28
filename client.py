import socket
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(server_address)

try:
    while True:
        message = input('\n⚡️  Ingrese entrada: ')
        if not message:
            break
        sock.sendall(message.encode())
finally:
    print('✅ Closing socket...')
    sock.close()
