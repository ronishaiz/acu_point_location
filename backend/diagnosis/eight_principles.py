
from enum import Enum


class InternalExternalPrinciple(Enum):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"


class FullEmptyPrinciple(Enum):
    FULL = "FULL"
    EMPTY = "EMPTY"


class HotColdPrinciple(Enum):
    HOT = "HOT"
    COLD = "COLD"


class YinYangPrinciple(Enum):
    YIN_PLUS = "YIN+"
    YANG_PLUS = "YANG+"
    YIN_MINUS = "YIN-"
    YANG_MINUS = "YANG-"

class EightPrinciples:
    intenal_external: InternalExternalPrinciple
    full_empty: FullEmptyPrinciple
    hot_cold: HotColdPrinciple = None
    yin_yang: YinYangPrinciple = None
