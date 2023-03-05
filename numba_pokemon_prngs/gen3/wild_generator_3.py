"""Generator for Gen 3 wild encounters"""

import numpy as np
from .state import GeneratorState
from ..compilation import optional_jitclass, array_type, TypedList
from ..enums import Method, Encounter, Lead, Game
from ..data.encounter.encounter_area_3 import EncounterArea3
from ..data.personal import get_info_table_3, PersonalInfo3
from ..lcrng import PokeRNGMod
from .util import unown_check, get_shiny
from . import encounter_area_3

rand_2880 = PokeRNGMod.const_rand(2880)
rand_2 = PokeRNGMod.const_rand(2)
rand_3 = PokeRNGMod.const_rand(3)
rand_25 = PokeRNGMod.const_rand(25)


@optional_jitclass
class WildGenerator3:
    """Generator for Gen 3 wild encounters"""

    method: np.uint8
    encounter: np.uint8
    game: np.uint8
    lead: np.uint8
    tsv: np.uint16
    personal_info_table: array_type(PersonalInfo3.dtype)

    def __init__(
        self,
        method: Method,
        encounter: Encounter,
        lead: Lead,
        game: Game,
        tid: np.uint16,
        sid: np.uint16,
    ) -> None:
        self.method = np.uint8(method)
        self.encounter = np.uint8(encounter)
        self.game = np.uint8(game)
        # leads only function in emerald
        self.lead = (
            np.uint8(lead) if (self.game & Game.EMERALD) else np.uint8(Lead.NONE)
        )
        self.tsv = np.uint16(tid ^ sid)
        self.personal_info_table = get_info_table_3(self.game)

    def cute_charm_check(self, pid: np.uint32, info: PersonalInfo3) -> np.bool_:
        """Check if a pid needs cute charm correction"""
        if self.lead == Lead.CUTE_CHARM_F:
            return (pid & 0xFF) >= info.gender_ratio
        return (pid & 0xFF) < info.gender_ratio

    def generate(
        self,
        seed: np.uint32,
        delay: np.uint32,
        initial_advances: np.uint32,
        max_advances: np.uint32,
        encounter_area: EncounterArea3,
    ) -> list[GeneratorState]:
        """Generate states from seed"""
        states = TypedList()
        modified_slots = TypedList()
        modified_slots.append(encounter_area.land[0])
        modified_slots = encounter_area_3.get_modified_slots(
            encounter_area,
            self.encounter,
            self.lead,
            self.game,
            self.personal_info_table,
        )
        rate = encounter_area_3.get_encounter_rate(encounter_area, self.encounter) * 16
        rse_safari = encounter_area_3.is_rse_safari_zone(encounter_area, self.game)
        rse = self.game & (Game.RUBY | Game.SAPPHIRE | Game.EMERALD)
        cute_charm = False
        rng = PokeRNGMod(seed)
        go = PokeRNGMod(0)
        rng.jump(initial_advances + delay)
        for advance in range(initial_advances, initial_advances + max_advances):
            go.re_init(rng.seed)

            # RSE uses main rng to check for rock smash encounters
            if rse and self.encounter == Encounter.ROCK_SMASH and rand_2880(go) >= rate:
                continue

            encounter_slot = encounter_area_3.calculate_hslot_lead(
                encounter_area, go, self.encounter, self.lead, modified_slots
            )
            species = encounter_slot.species & 0x7FF
            form = encounter_slot.species >> 11
            level = encounter_area_3.calculate_level(
                encounter_slot, go, self.lead == Lead.PRESSURE
            )
            info = self.personal_info_table[species]
            if self.lead == Lead.CUTE_CHARM_M or self.lead == Lead.CUTE_CHARM_F:
                if 0 < info.gender_ratio < 254:
                    cute_charm = False
                else:
                    cute_charm = rand_3(go) != 0

            # pokeblocks
            if rse_safari:
                go.next()

            if self.lead <= Lead.SYNCHRONIZE_QUIRKY:
                search_nature = self.lead if rand_2(go) == 0 else rand_25(go)
            else:
                search_nature = rand_25(go)

            pid = go.next_u16() | (go.next_u16() << 16)
            while (
                ((pid % 25) != search_nature)
                or (cute_charm and not self.cute_charm_check(pid, info))
                or (species == 201 and not unown_check(pid, form))
            ):
                pid = go.next_u16() | (go.next_u16() << 16)

            if self.method == Method.METHOD_2:
                go.next()
            iv1 = go.next_u16()
            if self.method == Method.METHOD_4:
                go.next()
            iv2 = go.next_u16()

            ivs = np.empty(6, np.uint8)
            ivs[0] = iv1 & 0x1F
            ivs[1] = (iv1 >> 5) & 0x1F
            ivs[2] = (iv1 >> 10) & 0x1F
            ivs[3] = (iv2 >> 5) & 0x1F
            ivs[4] = (iv2 >> 10) & 0x1F
            ivs[5] = iv2 & 0x1F

            state = GeneratorState(
                advance,
                pid,
                species,
                form,
                ivs,
                pid & 1,
                level,
                get_shiny(pid, self.tsv),
                info,
            )

            states.append(state)

            rng.next()

        return states
