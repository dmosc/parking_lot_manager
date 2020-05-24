import time
from utils import constants


class Request:
    def __init__(self, data, opened_at):
        request = data.split(' ')
        self.time = int(round(time.time() - (opened_at if opened_at is not None else 0)))
        self.operation = request[0]

        if self.operation == constants.OPENING:
            [_, spots, in_doors, out_doors] = request
            self.time = 0
            self.spots = spots
            self.in_doors = in_doors
            self.out_doors = out_doors
        elif self.operation == constants.INSERT_TICKET:
            [_, door, is_ticket_paid] = request
            self.door = door
            self.is_ticket_paid = is_ticket_paid
        else:
            [_, door] = request
            self.door = door

    def print_content(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))
