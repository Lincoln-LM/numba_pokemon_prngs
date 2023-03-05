"""PersonalInfo for each Generation"""

import numpy as np
from ..util import DTypeDataclass, dtype_dataclass, unused_bytes, U8, U16


class PersonalInfoProtocol(DTypeDataclass):
    """Protocol for a generic PersonalInfo class"""

    dtype: np.dtype
    ability_1: U8
    ability_2: U8
    ability_h: U8
    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    gender_ratio: U8


@dtype_dataclass
class PersonalInfo1:
    """PersonalInfo for Generation 1"""

    gender_ratio: U8
    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    base_exp: U8
    _padding: unused_bytes(6)
    move_1: U8
    move_2: U8
    move_3: U8
    move_4: U8
    exp_growth: U8
    tm_hm: unused_bytes(7)


PersonalInfo1.dtype: np.dtype
assert PersonalInfo1.dtype.itemsize == 0x1C


@dtype_dataclass
class PersonalInfo2:
    """PersonalInfo for Generation 2"""

    dex_id: U8
    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    base_exp: U8
    item_1: U8
    item_2: U8
    gender_ratio: U8
    hatch_cycles: U8
    _padding: unused_bytes(7)
    exp_growth: U8
    egg_group: U8
    tm_hm: unused_bytes(8)


PersonalInfo2.dtype: np.dtype
assert PersonalInfo2.dtype.itemsize == 0x20


@dtype_dataclass
class PersonalInfo3:
    """PersonalInfo for Generation 3"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    base_exp: U8
    ev_yield: U16
    item_1: U16
    item_2: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U8
    ability_2: U8
    escape_rate: U8
    misc: unused_bytes(3)


PersonalInfo3.dtype: np.dtype
assert PersonalInfo3.dtype.itemsize == 0x1C


@dtype_dataclass
class PersonalInfo4:
    """PersonalInfo for Generation 4"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    base_exp: U8
    ev_yield: U16
    item_1: U16
    item_2: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U8
    ability_2: U8
    escape_rate: U8
    misc: unused_bytes(3)
    tm_hm: unused_bytes(13)
    # Manually added attributes
    form_count: U8
    form_stats_index: U16


PersonalInfo4.dtype: np.dtype
assert PersonalInfo4.dtype.itemsize == 0x2C


@dtype_dataclass
class PersonalInfo5BW:
    """PersonalInfo for Generation 5 Black and White"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    evo_stage: U8
    ev_yield: U16
    item_1: U16
    item_2: U16
    item_3: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U8
    ability_2: U8
    ability_h: U8
    escape_rate: U8
    form_stats_index: U16
    form_sprite: U16
    form_count: U8
    misc: U8
    base_exp: U16
    height: U16
    weight: U16
    tm_hm: unused_bytes(16)
    type_tutors: unused_bytes(4)


PersonalInfo5BW.dtype: np.dtype
assert PersonalInfo5BW.dtype.itemsize == 0x3C


@dtype_dataclass
class PersonalInfo5B2W2:
    """PersonalInfo for Generation 5 Black 2 and White 2"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    evo_stage: U8
    ev_yield: U16
    item_1: U16
    item_2: U16
    item_3: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U8
    ability_2: U8
    ability_h: U8
    escape_rate: U8
    form_stats_index: U16
    form_sprite: U16
    form_count: U8
    misc: U8
    base_exp: U16
    height: U16
    weight: U16
    tm_hm: unused_bytes(16)
    type_tutors: unused_bytes(4)
    specific_tutors: unused_bytes(16)


PersonalInfo5B2W2.dtype: np.dtype
assert PersonalInfo5B2W2.dtype.itemsize == 0x4C


@dtype_dataclass
class PersonalInfo6XY:
    """PersonalInfo for Generation 6 X and Y"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    evo_stage: U8
    ev_yield: U16
    item_1: U16
    item_2: U16
    item_3: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U8
    ability_2: U8
    ability_h: U8
    escape_rate: U8
    form_stats_index: U16
    form_sprite: U16
    form_count: U8
    misc: U8
    base_exp: U16
    height: U16
    weight: U16
    tm_hm: unused_bytes(16)
    type_tutors: unused_bytes(8)


PersonalInfo6XY.dtype: np.dtype
assert PersonalInfo6XY.dtype.itemsize == 0x40


@dtype_dataclass
class PersonalInfo6AO:
    """PersonalInfo for Generation 6 Omega Ruby and Alpha Sapphire"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    evo_stage: U8
    ev_yield: U16
    item_1: U16
    item_2: U16
    item_3: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U8
    ability_2: U8
    ability_h: U8
    escape_rate: U8
    form_stats_index: U16
    form_sprite: U16
    form_count: U8
    misc: U8
    base_exp: U16
    height: U16
    weight: U16
    tm_hm: unused_bytes(16)
    type_tutors: unused_bytes(8)
    specific_tutors: unused_bytes(16)


PersonalInfo6AO.dtype: np.dtype
assert PersonalInfo6AO.dtype.itemsize == 0x50


@dtype_dataclass
class PersonalInfo7:
    """PersonalInfo for Generation 7"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    evo_stage: U8
    ev_yield: U16
    item_1: U16
    item_2: U16
    item_3: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U8
    ability_2: U8
    ability_h: U8
    escape_rate: U8
    form_stats_index: U16
    form_sprite: U16
    form_count: U8
    misc: U8
    base_exp: U16
    height: U16
    weight: U16
    tm: unused_bytes(16)
    type_tutors: unused_bytes(4)
    specific_tutors: unused_bytes(16)
    special_z_item: U16
    special_z_base_move: U16
    special_z_move: U16
    local_variant: U8
    _padding: unused_bytes(1)


PersonalInfo7.dtype: np.dtype
assert PersonalInfo7.dtype.itemsize == 0x54


@dtype_dataclass
class PersonalInfo7GG:
    """PersonalInfo for Let's Go Pikachu and Eevee"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    evo_stage: U8
    ev_yield: U16
    item_1: U16
    item_2: U16
    item_3: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U8
    ability_2: U8
    ability_h: U8
    escape_rate: U8
    form_stats_index: U16
    form_sprite: U16
    form_count: U8
    misc: U8
    base_exp: U16
    height: U16
    weight: U16
    tm: unused_bytes(32)
    go_species: U16
    _padding_0: unused_bytes(2)
    special_z_item: U16
    special_z_base_move: U16
    special_z_move: U16
    local_variant: U8
    _padding_1: unused_bytes(1)


PersonalInfo7GG.dtype: np.dtype
assert PersonalInfo7GG.dtype.itemsize == 0x54


@dtype_dataclass
class PersonalInfo8SWSH:
    """PersonalInfo for Generation 8 Sword and Shield"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    evo_stage: U8
    ev_yield: U16
    item_1: U16
    item_2: U16
    item_3: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U16
    ability_2: U16
    ability_h: U16
    form_stats_index: U16
    form_count: U8
    misc: U8
    base_exp: U16
    height: U16
    weight: U16
    tm: unused_bytes(16)
    type_tutors: unused_bytes(4)
    tr: unused_bytes(16)
    species: U16
    _padding_0: unused_bytes(8)
    hatch_species: U16
    local_form_index: U16
    regional_flags: U16
    pokedex_index: U16
    regional_form_index: U16
    _padding_1: unused_bytes(72)
    armor_tutor: unused_bytes(4)
    armor_dex_index: U16
    crown_dex_index: U16


PersonalInfo8SWSH.dtype: np.dtype
assert PersonalInfo8SWSH.dtype.itemsize == 0xB0


@dtype_dataclass
class PersonalInfo8BDSP:
    """PersonalInfo for Generation 8 Brilliant Diamond and Shining Pearl"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    evo_stage: U8
    ev_yield: U16
    item_1: U16
    item_2: U16
    item_3: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U16
    ability_2: U16
    ability_h: U16
    form_stats_index: U16
    form_count: U8
    misc: U8
    base_exp: U16
    height: U16
    weight: U16
    tm: unused_bytes(16)
    type_tutors: unused_bytes(4)
    species: U16
    hatch_species: U16
    hatch_form_index: U16
    pokedex_index: U16


PersonalInfo8BDSP.dtype: np.dtype
assert PersonalInfo8BDSP.dtype.itemsize == 0x44


@dtype_dataclass
class PersonalInfo8LA:
    """PersonalInfo for Generation 8 Pokemon: Legends Arceus"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    evo_stage: U8
    ev_yield: U16
    item_1: U16
    item_2: U16
    item_3: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U16
    ability_2: U16
    ability_h: U16
    form_stats_index: U16
    form_count: U8
    misc: U8
    base_exp: U16
    height: U16
    weight: U16
    _padding_0: unused_bytes(46)
    hatch_species: U16
    hatch_form_index: U16
    regional_flags: U16
    species: U16
    form: U16
    dex_index_hisui: U16
    dex_index_hisui_local_1: U16
    dex_index_hisui_local_2: U16
    dex_index_hisui_local_3: U16
    dex_index_hisui_local_4: U16
    dex_index_hisui_local_5: U16
    _padding_1: unused_bytes(60)
    move_shop: unused_bytes(8)


PersonalInfo8LA.dtype: np.dtype
assert PersonalInfo8LA.dtype.itemsize == 0xB0


@dtype_dataclass
class PersonalInfo9SV:
    """PersonalInfo for Generation 9 Scarlet and Violet"""

    hp: U8
    attack: U8
    defense: U8
    speed: U8
    special_attack: U8
    special_defense: U8
    type_1: U8
    type_2: U8
    catch_rate: U8
    evo_stage: U8
    ev_yield: U16
    gender_ratio: U8
    hatch_cycles: U8
    base_friendship: U8
    exp_growth: U8
    egg_group_1: U8
    egg_group_2: U8
    ability_1: U16
    ability_2: U16
    ability_h: U16
    form_stats_index: U16
    form_count: U8
    misc: U8
    is_present_in_game: U8
    dex_group: U8
    dex_index: U16
    height: U16
    weight: U16
    hatch_species: U16
    local_form_index: U16
    regional_flags: U16
    regional_form_index: U16
    tm: unused_bytes(24)


PersonalInfo9SV.dtype: np.dtype
assert PersonalInfo9SV.dtype.itemsize == 0x44
