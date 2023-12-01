from enum import Enum

class Payoffs(Enum):
    WON_GAME = 20
    LOST_GAME = -10
    GAINED_VALID_OPTIONS_PER_CARD = 1
    LOST_VALID_OPTIONS_PER_CARD = -1