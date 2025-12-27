
from dataclasses import dataclass
from enum import Enum
from typing import List


class Speed(Enum):
    RAPID = "RAPID"
    SLOW = "SLOW"
    REGULAR = "REGULAR"


class Depth(Enum):
    FLOATING = "FLOATING"
    DEEP = "DEEP"
    SHALLOW = "SHALLOW"
    REGULAR = "REGULAR"


class Strength(Enum):
    V = "V"
    FULL = "V+"
    WEAK = "V-"


class Quality(Enum):
    WIRY = "WIRY"
    SLIPPERY = "SLIPPERY"
    CHOPPY = "CHOPPY"
    THIN = "THIN"
    FLOODING = "FLOODING"
    TENSE = "TENSE"
    HIDDEN = "HIDDEN"
    EMPTY = "EMPTY"


class PositionYinYang(Enum):
    YIN = "YIN"
    YANG = "YANG"


class PositionJiao(Enum):
    UJ = "UJ"
    MJ = "MJ"
    LJ = "LJ"


class PositionHand(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


@dataclass
class PulsePosition:
    yin_yang: PositionYinYang
    jiao: PositionJiao
    left_right: PositionHand


@dataclass
class Pulse:

    _speed: Speed
    _depth: Depth
    _strength: Strength
    _quality: List[Quality]
    _positions: List[PulsePosition] = None
