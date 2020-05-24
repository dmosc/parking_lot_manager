import socket
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(server_address)

try:
    messages = [
        'opening 3 2 2',
        'button_press 1',
        'withdraw_ticket 1',
        'laser_off_in 1',
        'laser_on_in 1',
        'insert_ticket 1 0',
        'insert_ticket 1 1',
        'laser_off_out 1',
        'laser_on_out 1',
        'closing'
    ]

    while True:
        message = input('\n⚡️  Ingrese entrada: ')
        if not message:
            break

        print(message)
        sock.sendall(message.encode())
        # data = sock.recv(30)

finally:
    print('✅ Closing socket...')
    sock.close()
