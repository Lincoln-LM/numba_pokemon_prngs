"""Enum for various generation methods"""

from enum import IntEnum


class Method(IntEnum):
    """Enum for various generation methods"""

    NONE = 0

    METHOD_1 = 1
    METHOD_1_REVERSE = 2
    METHOD_2 = 3
    METHOD_4 = 4

    XD_COLO = 5
    CHANNEL = 6

    EBRED = 7
    EBRED_SPLIT = 8
    EBRED_ALTERNATE = 9
    EBRED_PID = 10
    RSFRLGBRED = 11
    RSFRLGBRED_SPLIT = 12
    RSFRLGBRED_ALTERNATE = 13
    RSFRLGBRED_MIXED = 14

    CUTE_CHARM_DPPT = 15
    CUTE_CHARM_HGSS = 16
    METHOD_J = 17
    METHOD_K = 18
    POKERADAR = 19
    WONDERCARD_IVS = 20

    METHOD_5_IVS = 21
    METHOD_5_CGEAR = 22
    METHOD_5 = 23
