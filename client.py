import socket
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(server_address)

try:
    messages = ['0.00 apertura 2 2 1',
                '1.00 oprimeBoton 1',
                '27.00 meteTarjeta 1 1',
                '44.00 oprimeBoton 1',
                '44.00 oprimeBoton 2',
                '51.00 recogeTarjeta 1',
                '51.00 recogeTarjeta 2',
                '58.00 laserOffE 1',
                '58.00 laserOffE 2',
                '59.00 laserOnE 1',
                '59.00 laserOnE 2',
                '66.00 oprimeBoton 1',
                '71.00 oprimeBoton 1',
                '73.00 meteTarjeta 1 1',
                '82.00 oprimeBoton 1',
                '96.00 laserOnE 1',
                '97.00 meteTarjeta 1 1',
                '110.00 cierre']
    globalTime = 0.00
    for message in messages:
        timestamp = float(message[0:4])
        payload = message[message.index(" ") + 1:]
        toSleep = timestamp - globalTime
        time.sleep(toSleep)
        globalTime += toSleep
        print('client sending "%s"' % payload)
        print(payload)
        sock.sendall(payload.encode())
        # response = sock.recv(256)
finally:
    print('✅ Closing socket...')
    sock.close()
