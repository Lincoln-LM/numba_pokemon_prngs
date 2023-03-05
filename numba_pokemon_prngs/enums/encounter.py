"""Enum for various encounter types"""

from enum import IntEnum


class Encounter(IntEnum):
    """Enum for various encounter types"""

    GRASS = 0
    DOUBLE_GRASS = 1
    SPECIAL_GRASS = 2
    ROCK_SMASH = 3
    SURFING = 4
    SPECIAL_SURF = 5
    OLD_ROD = 6
    GOOD_ROD = 7
    SUPER_ROD = 8
    SPECIAL_SUPER_ROD = 9
    STATIC = 10
    BUG_CATCHING_CONTEST = 11
    HEADBUTT = 12
    HEADBUTT_ALT = 13
    HEADBUTT_SPECIAL = 14
    ROAMER = 15
    GIFT = 16
    ENTRALINK = 17
    GIFT_EGG = 18
    HIDDEN_GROTTO = 19
