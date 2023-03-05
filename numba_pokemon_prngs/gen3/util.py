"""Utility functions for gen 3"""

import numpy as np
from ..compilation import optional_njit, return_type


@optional_njit(return_type(np.uint8, (np.uint32, np.uint8)))
def get_gender(pid: np.uint32, gender_ratio: np.uint8):
    """Get gender based on pid and gender ratio"""
    if gender_ratio == 255:
        return 2
    if gender_ratio == 254:
        return 1
    if gender_ratio == 0:
        return 0
    return (pid & 0xFF) < gender_ratio


@optional_njit(return_type(np.uint8, (np.uint32, np.uint16)))
def get_shiny(pid: np.uint32, tsv: np.uint16):
    """Get shiny type based on pid and full tsv"""
    psv = (pid >> 16) ^ (pid & 0xFFFF)
    if tsv == psv:
        return 2
    if (tsv ^ psv) < 8:
        return 1
    return 0


@optional_njit(return_type(np.bool_, (np.uint32, np.uint8)))
def unown_check(pid: np.uint32, form: np.uint8):
    """Verify unown form"""
    letter = (
        ((pid & 0x3000000) >> 18)
        | ((pid & 0x30000) >> 12)
        | ((pid & 0x300) >> 6)
        | (pid & 0x3)
    ) % 0x1C
    return letter == form
