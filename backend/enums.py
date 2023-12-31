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

    hui_meeting_of_vessels: str = 'HUI MEETING OF VESSELS'

    horary: str = 'HORARY'

    window_of_heaven: str = 'WINDOW OF HEAVEN'

    luo: str = 'LUO'  # Hibur

    xi: str = 'XI'  # Hitstabrut

    mu: str = 'MU'  # Hatra'a

    ren_mai_opening: str = 'REN MAI OPENING'

    command: str = 'COMMAND'

    stage_meeting: str = 'STAGE MEETING'
