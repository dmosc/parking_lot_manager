import socket

from classes import Request, ParkingLot
from utils import TableIt, constants, functions

PORT = 10000
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', PORT)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

sock.listen(1)

# Wait for connections
print('🚀  Listening on port: %s' % str(PORT))

# Basic setup
parking_lot = ParkingLot.ParkingLot(0, 0)
opened_at = None

while True:
    [connection, client_address] = sock.accept()
    print(client_address)
    try:
        while True:
            payload = connection.recv(30)
            decoded_payload = payload.decode()
            if len(decoded_payload) > 0:
                request = Request.Request(decoded_payload, opened_at)

                if request.operation == constants.OPENING:
                    parking_lot.open(request)
                    opened_at = parking_lot.opened_at
                elif request.operation == constants.CLOSING:
                    parking_lot.close()
                    parking_lot.log.append([request.time, decoded_payload, '', parking_lot.spots._value])
                    break

                if parking_lot.is_open:
                    door_type = constants.DOOR_TYPE_OPERATION.get(request.operation, 'INVALID_OPERATION')
                    door = request.door if hasattr(request, 'door') else -1
                    total_in_doors = len(parking_lot.in_doors)
                    total_out_doors = len(parking_lot.out_doors)

                    if door_type == -1 or functions.is_door_valid(door, door_type, total_in_doors, total_out_doors):
                        if door_type == 0:
                            parking_lot.in_doors[int(request.door) - 1].request_queue.put(request)
                        elif door_type == 1:
                            parking_lot.out_doors[int(request.door) - 1].request_queue.put(request)
                        parking_lot.log.append([request.time, decoded_payload, '', parking_lot.spots._value])
                    else:
                        print('Door #%s is not valid!' % str(request.door))
                        parking_lot.log.append(
                            [request.time, '', 'Door #%s is not valid!' % str(request.door), parking_lot.spots._value])
                else:
                    print('❌  Parking lot is not open yet!')
                    parking_lot.log.append(['', '', '❌  Parking lot is not open yet!', parking_lot.spots._value])
            else:
                break
    finally:
        TableIt.printTable(parking_lot.log, useFieldNames=True)
        print('✅  Closing socket...')
        connection.close()

    break

# Cleanup and join threads
for entrance in parking_lot.in_doors:
    entrance.request_queue.join()
    entrance.request_queue.put(None)

for entrance in parking_lot.out_doors:
    entrance.request_queue.join()
    entrance.request_queue.put(None)

for thread in parking_lot.threads:
    thread.join()
