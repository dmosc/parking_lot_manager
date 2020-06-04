import time, threading
from classes import Entrance


class ParkingLot:
    is_open = False
    opened_at = 0
    busy_spots = 0
    spots = threading.BoundedSemaphore(0)
    in_doors = []
    out_doors = []
    threads = []
    log = [['Timestamp', 'Command', 'Log', 'Available spots', 'Busy spots']]

    def __init__(self, in_doors, out_doors):
        self.is_open = False
        self.init_doors(in_doors, out_doors)

    def open(self, request):
        self.is_open = True
        self.opened_at = int(round(time.time()))
        self.busy_spots = 0
        self.spots = threading.BoundedSemaphore(int(request.spots))
        self.init_doors(request.in_doors, request.out_doors)

    def close(self):
        self.is_open = False

    def init_doors(self, in_doors, out_doors):
        for i in range(int(in_doors)):
            entrance = Entrance.Entrance(self, i)
            thread = threading.Thread(target=entrance.process_request)
            thread.start()

            self.in_doors.append(entrance)
            self.threads.append(thread)

        for i in range(int(out_doors)):
            entrance = Entrance.Entrance(self, i)

            thread = threading.Thread(target=entrance.process_request)
            thread.start()

            self.out_doors.append(entrance)
            self.threads.append(thread)

    def print_content(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))

    def print_spots(self):
        print('Spots available: %s' % str(self.spots._value))
