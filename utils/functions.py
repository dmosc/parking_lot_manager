def is_door_valid(door, door_type, in_doors, out_doors):
    in_range = False
    if door_type == 0:
        in_range = int(door) <= in_doors
    elif door_type == 1:
        in_range = int(door) <= out_doors

    return in_range
