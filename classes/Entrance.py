import queue
import random
import time

from utils import constants


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
                self.button_press(request)
            elif request.operation == constants.WITHDRAW_TICKET:
                self.withdraw_ticket(request)
            elif request.operation == constants.INSERT_TICKET:
                self.insert_ticket(request)
            elif request.operation == constants.LASER_OFF_IN:
                self.laser_off_in(request)
            elif request.operation == constants.LASER_ON_IN:
                self.laser_on_in(request)
            elif request.operation == constants.LASER_OFF_OUT:
                self.laser_off_out(request)
            elif request.operation == constants.LASER_ON_OUT:
                self.laser_on_out(request)

            self.request_queue.task_done()

    # Routines
    def button_press(self, request):
        print('⏳  Looking for spot...')
        self.parking_lot.log.append([request.time, '', '⏳  Looking for spot...', self.parking_lot.spots._value, self.parking_lot.busy_spots])
        if self.parking_lot.spots.acquire(blocking=False):
            self.parking_lot.busy_spots += 1
            time.sleep(5)
            print('✅  Printing ticket...')
            t = int(round(time.time() - self.parking_lot.opened_at))
            self.parking_lot.log.append([t, '', '✅  Printing ticket...', self.parking_lot.spots._value, self.parking_lot.busy_spots])
        else:
            print('🔒  There are currently no spots available!')
            t = int(round(time.time() - self.parking_lot.opened_at))
            self.parking_lot.log.append(
                [t, '', '🔒  There are currently no spots available!', self.parking_lot.spots._value, self.parking_lot.busy_spots])

    def withdraw_ticket(self, request):
        print('✅  User is withdrawing ticket...')
        time.sleep(random.randint(1, 10))
        t = int(round(time.time() - self.parking_lot.opened_at))
        self.parking_lot.log.append(
            [t, '', '⏳  User is entering through parking pen #%s...' % request.door, self.parking_lot.spots._value, self.parking_lot.busy_spots])
        print('✅  Lifting parking pen...')
        time.sleep(5)
        t = int(round(time.time() - self.parking_lot.opened_at))
        self.parking_lot.log.append([t, '', '✅  Lifting parking pen...', self.parking_lot.spots._value, self.parking_lot.busy_spots])

    def insert_ticket(self, request):
        print('👁  Verifying ticket...')
        self.parking_lot.log.append([request.time, '', '👁  Verifying ticket...', self.parking_lot.spots._value, self.parking_lot.busy_spots])
        time.sleep(1)
        if int(request.is_ticket_paid) == 1:
            try:
                self.parking_lot.spots.release()
                self.parking_lot.busy_spots -= 1
                print('✅  Lifting parking pen...')
                time.sleep(5)
                t = int(round(time.time() - self.parking_lot.opened_at))
                self.parking_lot.log.append([t, '', '✅  Lifting parking pen...', self.parking_lot.spots._value, self.parking_lot.busy_spots])
            except ValueError:
                print('❌  Parking pen is not responding, request a supervisor!')
                self.parking_lot.log.append(
                    [request.time, '', '❌  Parking pen is not responding, request a supervisor!',
                     self.parking_lot.spots._value, self.parking_lot.busy_spots])
        else:
            print('❌  Ticket is pending to pay...')
            t = int(round(time.time() - self.parking_lot.opened_at))
            self.parking_lot.log.append([t, '', '❌  Ticket is pending to pay...', self.parking_lot.spots._value, self.parking_lot.busy_spots])

        self.parking_lot.print_spots()

    def laser_off_in(self, request):
        print('⏳  User is entering through parking pen #%s...' % request.door)
        self.parking_lot.log.append([request.time, '', '⏳  User is entering through parking pen #%s...' % request.door,
                                     self.parking_lot.spots._value, self.parking_lot.busy_spots])

    def laser_off_out(self, request):
        print('⏳  User is leaving through parking pen #%s...' % request.door)
        self.parking_lot.log.append([request.time, '', '⏳  User is leaving through parking pen #%s...' % request.door,
                                     self.parking_lot.spots._value, self.parking_lot.busy_spots])

    def laser_on_in(self, request):
        print('✅  User successfully entered through door #%s' % request.door)
        print('⏳  Reinstating parking pen...')
        time.sleep(5)
        t = int(round(time.time() - self.parking_lot.opened_at))
        self.parking_lot.log.append([request.time, '', '✅  User successfully entered through door #%s' % request.door,
                                     self.parking_lot.spots._value, self.parking_lot.busy_spots])
        self.parking_lot.log.append([t, '', '⏳  Reinstating parking pen...', self.parking_lot.spots._value, self.parking_lot.busy_spots])

    def laser_on_out(self, request):
        print('✅  User successfully exited through door #%s' % request.door)
        print('⏳  Reinstating parking pen...')
        time.sleep(5)
        t = int(round(time.time() - self.parking_lot.opened_at))
        self.parking_lot.log.append(
            [request.time, '', '✅  User successfully exited through door #%s' % request.door,
             self.parking_lot.spots._value, self.parking_lot.busy_spots])
        self.parking_lot.log.append([t, '', '⏳  Reinstating parking pen...', self.parking_lot.spots._value, self.parking_lot.busy_spots])
