import queue
import time
import random
from utils import constants


def laser_off_in(request):
    print('⏳  User is entering through parking pen #%s...' % request.door)


def laser_off_out(request):
    print('⏳  User is leaving through parking pen #%s...' % request.door)


def withdraw_ticket():
    print('✅  User is withdrawing ticket...')
    time.sleep(random.randint(1, 10))
    print('✅  Lifting parking pen...')
    time.sleep(5)


class Entrance:
    def __init__(self, parking_lot, number):
        self.number = number
        self.parking_lot = parking_lot
        self.request_queue = queue.Queue(100)

    def process_request(self):
        while True:
            request = self.request_queue.get()
            if request is None:
                break

            if request.operation == constants.BUTTON_PRESS:
                self.button_press()
            elif request.operation == constants.WITHDRAW_TICKET:
                withdraw_ticket()
            elif request.operation == constants.INSERT_TICKET:
                self.insert_ticket(request)
            elif request.operation == constants.LASER_OFF_IN:
                laser_off_in(request)
            elif request.operation == constants.LASER_ON_IN:
                self.laser_on_in(request)
            elif request.operation == constants.LASER_OFF_OUT:
                laser_off_out(request)
            elif request.operation == constants.LASER_ON_OUT:
                self.laser_on_out(request)

            self.request_queue.task_done()

    # Routines
    def button_press(self):
        print('⏳  Looking for spot...')
        self.parking_lot.log.append(['', '', '⏳  Looking for spot...', self.parking_lot.spots._value])
        if self.parking_lot.spots.acquire(blocking=False):
            print('✅  Printing ticket...')
            self.parking_lot.log.append(['', '', '✅  Printing ticket...', self.parking_lot.spots._value])
            time.sleep(5)
        else:
            print('🔒  There are currently no spots available!')
            self.parking_lot.log.append(['', '', '🔒  There are currently no spots available!', self.parking_lot.spots._value])

    def laser_on_in(self, request):
        print('✅  User successfully entered through door #%s' % request.door)
        print('⏳  Reinstating parking pen...')
        self.parking_lot.log.append(['', '', '✅  User successfully entered through door #%s' % request.door, self.parking_lot.spots._value])
        self.parking_lot.log.append(['', '', '⏳  Reinstating parking pen...', self.parking_lot.spots._value])
        time.sleep(5)
        self.parking_lot.print_spots()

    def laser_on_out(self, request):
        print('✅  User successfully exited through door #%s' % request.door)
        print('⏳  Reinstating parking pen...')
        self.parking_lot.log.append(['', '', '✅  User successfully exited through door #%s' % request.door, self.parking_lot.spots._value])
        self.parking_lot.log.append(['', '', '⏳  Reinstating parking pen...', self.parking_lot.spots._value])
        time.sleep(5)
        self.parking_lot.print_spots()

    def insert_ticket(self, request):
        print('👁  Verifying ticket...')
        self.parking_lot.log.append(['', '', '👁  Verifying ticket...', self.parking_lot.spots._value])
        time.sleep(1)
        if int(request.is_ticket_paid) == 1:
            try:
                self.parking_lot.spots.release()
                print('✅  Lifting parking pen...')
                self.parking_lot.log.append(['', '', '✅  Lifting parking pen...', self.parking_lot.spots._value])
                time.sleep(5)
            except ValueError:
                print('❌  Parking pen is not responding, request a supervisor!')
                self.parking_lot.log.append(['', '', '❌  Parking pen is not responding, request a supervisor!', self.parking_lot.spots._value])
        else:
            print('❌  Ticket is pending to pay...')
            self.parking_lot.log.append(['', '', '❌  Ticket is pending to pay...', self.parking_lot.spots._value])

        self.parking_lot.print_spots()
