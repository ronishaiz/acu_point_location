from enum import Enum


class Stage(Enum):

    tai_yang: str = "TAI YANG"
    yang_ming: str = "YANG MING"
    shao_yang: str = "SHAO YANG"
    tai_yin: str = "TAI YIN"
    shao_yin: str = "SHAO YIN"
    jue_yin: str = "JUE YIN"


class Organ(Enum):

    LIV: str = 'LIV'
    GB: str = 'GB'
    HT: str = 'HT'
    SI: str = 'SI'
    PC: str = 'PC'
    TW: str = 'TW'
    SP: str = 'SP'
    ST: str = 'ST'
    LU: str = 'LU'
    LI: str = 'LI'
    KID: str = 'KID'
    BL: str = 'BL'


class MeridianName(Enum):

    LIV: str = 'LIV'
    GB: str = 'GB'
    HT: str = 'HT'
    SI: str = 'SI'
    PC: str = 'PC'
    TW: str = 'TW'
    SP: str = 'SP'
    ST: str = 'ST'
    LU: str = 'LU'
    LI: str = 'LI'
    KID: str = 'KID'
    BL: str = 'BL'
    CV: str = 'CV'
    GV: str = 'GV'


class Element(Enum):

    WOOD: str = 'WOOD'
    FIRE: str = 'FIRE'
    EARTH: str = 'EARTH'
    METAL: str = 'METAL'
    WATER: str = 'WATER'


class Limb(Enum):

    HAND: str = 'HAND'
    LEG: str = 'LEG'


class PointCharacter(Enum):

    well: str = 'WELL'
    spring: str = 'SPRING'
    stream: str = 'STREAM'
    river: str = 'RIVER'
    sea: str = 'SEA'

    yuan: str = 'YUAN'

    tonification: str = 'TONIFICATION'
    sedation: str = 'SEDATION'

    horary: str = 'HORARY'

    window_of_heaven: str = 'WINDOW OF HEAVEN'

    luo: str = 'LUO'  # Hibur

    xi: str = 'XI'  # Hitstabrut

    mu: str = 'MU'  # Hatra'a
    back_shu: str = 'BACK SHU'

    special_meridian_opening: str = 'SPECIAL MERIDIAN OPENING'

    command: str = 'COMMAND'

    meeting: str = 'MEETING'
    hui: str = 'HUI'

    sea_of_qi: str = 'SEA OF QI'

    sea_of_blood: str = 'SEA OF BLOOD'

    sea_of_water_and_grain: str = 'SEA OF WATER AND GRAIN'

    sea_of_marrow: str = 'SEA OF MARROW'

    lower_sea: str = 'LOWER SEA'

    forbidden_in_pregnancy: str = 'FORBIDDEN IN PREGNANCY'
