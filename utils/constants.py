# OPENING = 'opening'
# CLOSING = 'closing'
# BUTTON_PRESS = 'button_press'
# INSERT_TICKET = 'insert_ticket'
# WITHDRAW_TICKET = 'withdraw_ticket'
# LASER_OFF_IN = 'laser_off_in'
# LASER_OFF_OUT = 'laser_off_out'
# LASER_ON_IN = 'laser_on_in'
# LASER_ON_OUT = 'laser_on_out'

OPENING = 'apertura'
CLOSING = 'cierre'
BUTTON_PRESS = 'oprimeBoton'
INSERT_TICKET = 'meteTarjeta'
WITHDRAW_TICKET = 'recogeTarjeta'
LASER_OFF_IN = 'laserOffE'
LASER_OFF_OUT = 'laserOffS'
LASER_ON_IN = 'laserOnE'
LASER_ON_OUT = 'laserOnS'

DOOR_TYPE_OPERATION = {
    OPENING: -1,
    CLOSING: -1,
    BUTTON_PRESS: 0,
    WITHDRAW_TICKET: 0,
    LASER_OFF_IN: 0,
    LASER_ON_IN: 0,
    INSERT_TICKET: 1,
    LASER_OFF_OUT: 1,
    LASER_ON_OUT: 1
}
