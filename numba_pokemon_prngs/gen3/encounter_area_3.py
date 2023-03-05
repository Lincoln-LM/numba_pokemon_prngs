"""Namespace for EncounterArea3 (..data.encounter.encounter_area_3) related functions"""

import numpy as np
from ..data.encounter.encounter_area_3 import EncounterArea3, Slot3
from ..data.personal import PersonalInfo3
from ..lcrng import PokeRNGMod
from ..compilation import (
    optional_njit,
    TypedList,
)
from ..enums import Encounter, Game, Lead


def compute_table(ranges: tuple[int], greater: bool = False) -> np.array:
    """Compute encounter slot lookup table"""
    table = np.empty(100, dtype=np.uint8)

    r_val = 99 if greater else 0
    for i, range_val in enumerate(ranges):
        for r_val in range(r_val, range_val, -1 if greater else 1):
            table[r_val] = i

    return table


GRASS_TABLE = compute_table((20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100))
OLD_ROD_TABLE = compute_table((70, 100))
GOOD_ROD_TABLE = compute_table((60, 80, 100))
SUPER_ROD_TABLE = compute_table((40, 80, 95, 99, 100))
ROCK_SMASH_AND_SURF_TABLE = compute_table((60, 90, 95, 99, 100))

hslot_rand = PokeRNGMod.const_rand(100)
rand_2 = PokeRNGMod.const_rand(2)


@optional_njit
def calculate_hslot(
    encounter_area: EncounterArea3, rng: PokeRNGMod, encounter_type: Encounter
) -> Slot3:
    """Calculate the Slot3 of the current rng"""
    if encounter_type == Encounter.OLD_ROD:
        return encounter_area.fish_old[OLD_ROD_TABLE[hslot_rand(rng)]]
    if encounter_type == Encounter.GOOD_ROD:
        return encounter_area.fish_good[GOOD_ROD_TABLE[hslot_rand(rng)]]
    if encounter_type == Encounter.SUPER_ROD:
        return encounter_area.fish_super[SUPER_ROD_TABLE[hslot_rand(rng)]]
    if encounter_type == Encounter.ROCK_SMASH:
        return encounter_area.rock[ROCK_SMASH_AND_SURF_TABLE[hslot_rand(rng)]]
    if encounter_type == Encounter.SURFING:
        return encounter_area.water[ROCK_SMASH_AND_SURF_TABLE[hslot_rand(rng)]]
    return encounter_area.land[GRASS_TABLE[hslot_rand(rng)]]


@optional_njit
def calculate_hslot_lead(
    encounter_area: EncounterArea3,
    rng: PokeRNGMod,
    encounter_type: Encounter,
    lead: Lead,
    modified_slots: list[Slot3],
) -> Slot3:
    """Calculate hslot accounting for magnet pull and static"""
    if (
        (lead == Lead.MAGNET_PULL or lead == Lead.STATIC)
        and rand_2(rng) == 0
        and len(modified_slots) != 0
    ):
        return modified_slots[rng.next_rand(len(modified_slots))]
    return calculate_hslot(encounter_area, rng, encounter_type)


@optional_njit
def calculate_level(slot: Slot3, rng: PokeRNGMod, pressure: bool) -> np.uint8:
    """Calculate the level of a pokemon taking into account modification from pressure"""
    minimum = slot.min_level
    maximum = slot.max_level
    level_range = maximum - minimum + 1
    rand = rng.next_rand(level_range)
    if pressure:
        if rand_2(rng) == 0:
            return maximum
        if rand != 0:
            rand -= 1
    return minimum + rand


@optional_njit
def is_rse_safari_zone(encounter_area: EncounterArea3, game: Game) -> np.bool_:
    """Check if a locaton is in the RSE safari zone"""
    location = encounter_area.location
    if game & (Game.RUBY | Game.SAPPHIRE):
        if (
            location == 90
            or location == 187
            or location == 89
            or location == 186
            or location == 92
            or location == 189
            or location == 91
            or location == 188
        ):
            return True
    elif game & Game.EMERALD:
        if (
            location == 73
            or location == 98
            or location == 74
            or location == 20
            or location == 97
            or location == 72
        ):
            return True
    return False


@optional_njit
def get_modified_slots(
    encounter_area: EncounterArea3,
    encounter_type: Encounter,
    lead: Lead,
    game: Game,
    personal_info_table: list[PersonalInfo3],
):
    """Get modified slots from type-specific leads"""
    encounters = TypedList()
    # encounters.append(encounter_area.land[0])

    if lead == Lead.MAGNET_PULL:
        lead_type = 8
    elif lead == Lead.STATIC:
        lead_type = (
            13
            if game
            & (
                Game.RUBY
                | Game.SAPPHIRE
                | Game.EMERALD
                | Game.FIRE_RED
                | Game.LEAF_GREEN
                | Game.DIAMOND
                | Game.PEARL
                | Game.PLATINUM
                | Game.HEART_GOLD
                | Game.SOUL_SILVER
            )
            else 12
        )
    elif lead == Lead.HARVEST:
        lead_type = 11
    elif lead == Lead.FLASH_FIRE:
        lead_type = 9
    elif lead == Lead.STORM_DRAIN:
        lead_type = 10
    else:
        return encounters

    # loop has to be repeated or TypedList breaks for some reason
    if encounter_type == Encounter.OLD_ROD:
        for slot in encounter_area.fish_old:
            info: PersonalInfo3 = personal_info_table[slot.species & 0x3FF]
            if info.type_1 == lead_type or info.type_2 == lead_type:
                encounters.append(slot)
    elif encounter_type == Encounter.GOOD_ROD:
        for slot in encounter_area.fish_good:
            info: PersonalInfo3 = personal_info_table[slot.species & 0x3FF]
            if info.type_1 == lead_type or info.type_2 == lead_type:
                encounters.append(slot)
    elif encounter_type == Encounter.SUPER_ROD:
        for slot in encounter_area.fish_super:
            info: PersonalInfo3 = personal_info_table[slot.species & 0x3FF]
            if info.type_1 == lead_type or info.type_2 == lead_type:
                encounters.append(slot)
    elif encounter_type == Encounter.ROCK_SMASH:
        for slot in encounter_area.rock:
            info: PersonalInfo3 = personal_info_table[slot.species & 0x3FF]
            if info.type_1 == lead_type or info.type_2 == lead_type:
                encounters.append(slot)
    elif encounter_type == Encounter.SURFING:
        for slot in encounter_area.water:
            info: PersonalInfo3 = personal_info_table[slot.species & 0x3FF]
            if info.type_1 == lead_type or info.type_2 == lead_type:
                encounters.append(slot)
    else:
        for slot in encounter_area.land:
            info: PersonalInfo3 = personal_info_table[slot.species & 0x3FF]
            if info.type_1 == lead_type or info.type_2 == lead_type:
                encounters.append(slot)

    return encounters


@optional_njit
def get_encounter_rate(
    encounter_area: EncounterArea3, encounter_type: Encounter
) -> np.uint8:
    """Get encounter rate"""
    if encounter_type == Encounter.GRASS:
        return encounter_area.fish_rate
    if encounter_type == Encounter.ROCK_SMASH:
        return encounter_area.rock_rate
    if encounter_type == Encounter.SURFING:
        return encounter_area.water_rate
    return encounter_area.land_rate
