"""Encounter Slot Area Specification for Generation 3"""

from typing import Annotated
import numpy as np
from ..util import dtype_array, dtype_dataclass, U8, U16


@dtype_dataclass
class Slot3:
    """Gen 3 Encounter Slot"""

    min_level: U8
    max_level: U8
    species: U16


Slot3.dtype: np.dtype


@dtype_dataclass
class EncounterArea3:
    """Gen 3 Encounter Slot Area"""

    location: U16
    land_rate: U8
    land: Annotated[list[Slot3], dtype_array(Slot3, 12)]
    water_rate: U8
    water: Annotated[list[Slot3], dtype_array(Slot3, 5)]
    rock_rate: U8
    rock: Annotated[list[Slot3], dtype_array(Slot3, 5)]
    fish_rate: U8
    fish_old: Annotated[list[Slot3], dtype_array(Slot3, 2)]
    fish_good: Annotated[list[Slot3], dtype_array(Slot3, 3)]
    fish_super: Annotated[list[Slot3], dtype_array(Slot3, 5)]


EncounterArea3.dtype: np.dtype
