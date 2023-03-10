"""Utility functions for the data submodule"""

from dataclasses import dataclass, fields
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    U8 = np.uint8
    U16 = np.uint16
    U32 = np.uint32
else:
    U8 = np.dtype("u1")
    U16 = np.dtype("<u2")
    U32 = np.dtype("<u4")


def dtype_dataclass(cls):
    """Decorator to turn a dataclass into a numpy dtype"""
    dataclass_cls = dataclass(cls)
    dataclass_cls.dtype = np.dtype(
        [(field.name, field.type) for field in fields(dataclass_cls)]
    )
    return dataclass_cls


def unused_bytes(size: int) -> np.dtype:
    """Numpy dtype for an unused byte array"""
    return np.dtype([("", U8, (size,))])
