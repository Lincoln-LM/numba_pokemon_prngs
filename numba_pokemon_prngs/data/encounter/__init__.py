"""Encounter data for Pokemon games"""

import re
import json
import importlib.resources as pkg_resources
import numpy as np
from .encounter_area_3 import EncounterArea3
from .. import CONSTANT_CASE_SPECIES_EN
from ...resources import encount
from ...enums import Game


ENCOUNTER_DATA_FILES = {
    Game.RUBY: "rs_wild_encounters.json",
    Game.SAPPHIRE: "rs_wild_encounters.json",
    Game.EMERALD: "e_wild_encounters.json",
    Game.FIRE_RED: "frlg_wild_encounters.json",
    Game.LEAF_GREEN: "frlg_wild_encounters.json",
}

UNOWN_ENCOUNTERS = {
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        27,
    ],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_LIPTOO_CHAMBER": [
        2,
        2,
        2,
        3,
        3,
        3,
        7,
        7,
        7,
        20,
        20,
        14,
    ],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_WEEPTH_CHAMBER": [
        13,
        13,
        13,
        13,
        18,
        18,
        18,
        18,
        8,
        8,
        4,
        4,
    ],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_DILFORD_CHAMBER": [
        15,
        15,
        11,
        11,
        9,
        9,
        17,
        17,
        17,
        16,
        16,
        16,
    ],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_SCUFIB_CHAMBER": [
        24,
        24,
        19,
        19,
        6,
        6,
        6,
        5,
        5,
        5,
        10,
        10,
    ],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_RIXY_CHAMBER": [
        21,
        21,
        21,
        22,
        22,
        22,
        23,
        23,
        12,
        12,
        1,
        1,
    ],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_VIAPOIS_CHAMBER": [
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        26,
    ],
}


def clean_map_string(map_string: str) -> str:
    """Clean a map string to be easily readable"""
    map_string = map_string.replace("MAP_", "").replace("_", " ")

    strings = map_string.split()
    for i, string in enumerate(strings):
        match = re.match(r"Route(\d+)", string, re.IGNORECASE)
        if match:
            strings[i] = f"Route {match[1]}"
        else:
            match = re.match(r"Room(\d+)", string, re.IGNORECASE)
            if match:
                strings[i] = f"Room {match[1]}"
            elif re.match(r"B(\d+)F", string):
                strings[i] = string
            elif re.match(r"(\d+)F", string):
                strings[i] = string
            elif re.match(r"(\d+)R", string):
                strings[i] = string
            else:
                strings[i] = string.capitalize()

    return " ".join(strings)


def load_encounter_3(game: Game) -> tuple[tuple[str], np.recarray]:
    """Load Gen 3 encounter data"""
    with pkg_resources.open_text(
        encount, ENCOUNTER_DATA_FILES[game]
    ) as wild_encounters:
        encounters = json.load(wild_encounters)["wild_encounter_groups"][0][
            "encounters"
        ]

    if game == Game.RUBY:
        encounters = tuple(filter(lambda x: "Ruby" in x["base_label"], encounters))
    elif game == Game.SAPPHIRE:
        encounters = tuple(filter(lambda x: "Sapphire" in x["base_label"], encounters))
    elif game == Game.FIRE_RED:
        encounters = tuple(filter(lambda x: "FireRed" in x["base_label"], encounters))
    elif game == Game.LEAF_GREEN:
        encounters = tuple(filter(lambda x: "LeafGreen" in x["base_label"], encounters))

    encounter_information = np.zeros(len(encounters), dtype=EncounterArea3.dtype).view(
        np.recarray
    )
    map_names = []
    for map_number, encounter in enumerate(encounters):

        if re.match(r"gAlteringCave[2-9]", encounter["base_label"]):
            map_names.append("")
            continue

        if re.search(r"AlteringCave_[2-9]", encounter["base_label"]):
            map_names.append("")
            continue

        if "Unused" in encounter["base_label"]:
            map_names.append("")
            continue

        map_names.append(clean_map_string(encounter["map"]))

        encounter_area: EncounterArea3 = encounter_information[map_number]
        encounter_area.location = map_number

        land_mons = "land_mons" in encounter
        water_mons = "water_mons" in encounter
        rock_smash_mons = "rock_smash_mons" in encounter
        fishing_mons = "fishing_mons" in encounter

        if land_mons:
            encounter_area.land_rate = encounter["land_mons"]["encounter_rate"]
            for i, slot in enumerate(encounter["land_mons"]["mons"]):
                encounter_slot = encounter_area.land[i]
                encounter_slot.min_level = slot["min_level"]
                encounter_slot.max_level = slot["max_level"]
                encounter_slot.species = CONSTANT_CASE_SPECIES_EN.index(slot["species"])
                if encounter["map"] in UNOWN_ENCOUNTERS:
                    form = UNOWN_ENCOUNTERS[encounter["map"]][i]
                    encounter_slot.species |= form << 11
        if water_mons:
            encounter_area.water_rate = encounter["water_mons"]["encounter_rate"]
            for i, slot in enumerate(encounter["water_mons"]["mons"]):
                encounter_slot = encounter_area.water[i]
                encounter_slot.min_level = slot["min_level"]
                encounter_slot.max_level = slot["max_level"]
                encounter_slot.species = CONSTANT_CASE_SPECIES_EN.index(slot["species"])
        if rock_smash_mons:
            encounter_area.rock_rate = encounter["rock_smash_mons"]["encounter_rate"]
            for i, slot in enumerate(encounter["rock_smash_mons"]["mons"]):
                encounter_slot = encounter_area.rock[i]
                encounter_slot.min_level = slot["min_level"]
                encounter_slot.max_level = slot["max_level"]
                encounter_slot.species = CONSTANT_CASE_SPECIES_EN.index(slot["species"])
        if fishing_mons:
            encounter_area.fish_rate = encounter["fishing_mons"]["encounter_rate"]
            for i, slot in enumerate(encounter["fishing_mons"]["mons"]):
                if i < 2:
                    encounter_slot = encounter_area.fish_old[i]
                elif i < 5:
                    encounter_slot = encounter_area.fish_good[i - 2]
                else:
                    encounter_slot = encounter_area.fish_super[i - 5]
                encounter_slot.min_level = slot["min_level"]
                encounter_slot.max_level = slot["max_level"]
                encounter_slot.species = CONSTANT_CASE_SPECIES_EN.index(slot["species"])

    return tuple(map_names), encounter_information


MAP_NAMES_RUBY, ENCOUNTER_INFORMATION_RUBY = load_encounter_3(Game.RUBY)
MAP_NAMES_SAPPHIRE, ENCOUNTER_INFORMATION_SAPPHIRE = load_encounter_3(Game.SAPPHIRE)
MAP_NAMES_EMERALD, ENCOUNTER_INFORMATION_EMERALD = load_encounter_3(Game.EMERALD)
MAP_NAMES_FIRE_RED, ENCOUNTER_INFORMATION_FIRE_RED = load_encounter_3(Game.FIRE_RED)
MAP_NAMES_LEAF_GREEN, ENCOUNTER_INFORMATION_LEAF_GREEN = load_encounter_3(
    Game.LEAF_GREEN
)

MAP_NAMES_GEN3 = {
    Game.RUBY: MAP_NAMES_RUBY,
    Game.SAPPHIRE: MAP_NAMES_SAPPHIRE,
    Game.EMERALD: MAP_NAMES_EMERALD,
    Game.FIRE_RED: MAP_NAMES_FIRE_RED,
    Game.LEAF_GREEN: MAP_NAMES_LEAF_GREEN,
}

ENCOUNTER_INFORMATION_GEN3 = {
    Game.RUBY: ENCOUNTER_INFORMATION_RUBY,
    Game.SAPPHIRE: ENCOUNTER_INFORMATION_SAPPHIRE,
    Game.EMERALD: ENCOUNTER_INFORMATION_EMERALD,
    Game.FIRE_RED: ENCOUNTER_INFORMATION_FIRE_RED,
    Game.LEAF_GREEN: ENCOUNTER_INFORMATION_LEAF_GREEN,
}
