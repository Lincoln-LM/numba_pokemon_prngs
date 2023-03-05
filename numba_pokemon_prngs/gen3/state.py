"""Encounter State Information"""

import numpy as np
from ..compilation import optional_jitclass, array_type
from ..data.personal import PersonalInfoProtocol
from ..data import SPECIES_EN, ABILITIES_EN, NATURES_EN, TYPES_EN, GENDER_SYMBOLS
from ..util import compute_stat, hex_32
from .util import get_gender


# internal ordering of ivs
ORDER = np.array((0, 1, 2, 5, 3, 4), np.uint8)
# repeated to eliminate modulo
CHAR_ORDER = np.array((0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4), np.uint8)


class State:
    """Encounter State Information Parent Class"""

    pid: np.uint32
    species: np.uint16
    form: np.uint8
    stats: array_type(np.uint16)
    ability_index: np.uint16
    ivs: array_type(np.uint8)
    ability: np.uint8
    characteristic: np.uint8
    gender: np.uint8
    hidden_power: np.uint8
    hidden_power_strength: np.uint8
    level: np.uint8
    nature: np.uint8
    shiny: np.uint8

    def update_stats(self, info: PersonalInfoProtocol) -> None:
        """Update stats on initialization"""
        self.gender = get_gender(self.pid, info.gender_ratio)
        self.nature = self.pid % 25
        hidden_power_val = np.uint8(0)
        hidden_power_strength_value = np.uint8(0)
        ec_index = self.pid % np.uint8(6)
        char_index = ec_index
        max_iv = np.uint8(0)
        base_stats = (
            info.hp,
            info.attack,
            info.defense,
            info.special_attack,
            info.special_defense,
            info.speed,
        )

        for i in range(6):
            hidden_power_val += (self.ivs[ORDER[i]] & 1) << i
            hidden_power_strength_value += ((self.ivs[ORDER[i]] >> 1) & 1) << i

            stat = np.uint16(((2 * base_stats[i] + self.ivs[i]) * self.level) // 100)
            if i == 0:
                self.stats[i] = stat + self.level + 10
            else:
                self.stats[i] = compute_stat(stat + 5, self.nature, i)

            index = CHAR_ORDER[ec_index + i]
            if self.ivs[ORDER[index]] > max_iv:
                char_index = index
                max_iv = self.ivs[ORDER[index]]

        self.hidden_power = hidden_power_val * 15 // 63
        self.hidden_power_strength = 30 + (hidden_power_strength_value * 40 / 63)
        self.characteristic = (char_index * 5) + (max_iv % 5)


@optional_jitclass
class GeneratorState(State):
    """Encounter State Information for a generator"""

    advance: np.uint32

    def __init__(
        self,
        advance: np.uint32,
        pid: np.uint32,
        species: np.uint16,
        form: np.uint8,
        ivs: array_type(np.uint8),
        ability: np.uint8,
        level: np.uint8,
        shiny: np.uint8,
        info: PersonalInfoProtocol,
    ) -> None:
        self.advance = np.uint32(advance)
        self.pid = np.uint32(pid)
        self.species = np.uint16(species)
        self.form = np.uint8(form)
        self.ivs = np.empty(6, np.uint8)
        self.ivs[:] = ivs
        self.ability = np.uint8(ability)
        # no HA in g3
        self.ability_index = info.ability_1 if ability == 0 else info.ability_2
        self.level = np.uint8(level)
        self.shiny = np.uint8(shiny)
        self.stats = np.empty(6, np.uint16)
        self.update_stats(info)

    def csv(self) -> tuple[tuple[str, str]]:
        """Get a tuple representing the fields and values of the state as str"""
        return (
            ("Advance", str(self.advance)),
            (
                "Species",
                SPECIES_EN[self.species] + (f"-{self.form}" if self.form else ""),
            ),
            ("Level", str(self.level)),
            ("PID", hex_32(self.pid)),
            ("Nature", NATURES_EN[self.nature]),
            ("Ability", f"{ABILITIES_EN[self.ability_index]} ({self.ability})"),
            (
                "IVs",
                (
                    f"{self.ivs[0]}/"
                    f"{self.ivs[1]}/"
                    f"{self.ivs[2]}/"
                    f"{self.ivs[3]}/"
                    f"{self.ivs[4]}/"
                    f"{self.ivs[5]}"
                ),
            ),
            (
                "Stats",
                (
                    f"{self.stats[0]}/"
                    f"{self.stats[1]}/"
                    f"{self.stats[2]}/"
                    f"{self.stats[3]}/"
                    f"{self.stats[4]}/"
                    f"{self.stats[5]}"
                ),
            ),
            ("HP", f"{TYPES_EN[self.hidden_power+1]} ({self.hidden_power_strength})"),
            ("Gender", GENDER_SYMBOLS[self.gender]),
        )

    def __str__(self) -> str:
        str_repr = ""
        for field, value in self.csv():
            str_repr += f"{field}: {value}, "
        return str_repr[:-2]
