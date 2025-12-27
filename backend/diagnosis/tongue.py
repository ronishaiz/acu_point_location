

from dataclasses import dataclass
from enum import Enum
from typing import List


class BodyColor(Enum):
    PALE = "PALE"
    PINK = "PINK / LIGHT RED"
    RED = "RED"
    DARK_RED = "DARK_RED"
    PURPLE = "PURPLE"


class BodyShape(Enum):
    THIN = "THIN"
    SWOLLEN = "SWOLLEN"
    TEETH_MARKS = "TEETH MARKS"
    HORIZONTAL_CRACKS = "HORIZONTAL CRACKS"
    VERTICAL_CRACKS = "VERTICAL CRACKS"
    STIFF = "STIFF"
    DEVIATED = "DEVIATED"
    SUNKEN = "SUNKEN"
    REGULAR = "REGULAR"


class CoatingColor(Enum):
    WHITE = "WHITE"
    YELLOW = "YELLOW"
    GRAY = "GRAY"
    BLACK = "BLACK"
    TRANSPARENT = "TRANSPARENT"


class CoatingThickness(Enum):
    THIN = "THIN"
    THICK = "THICK"
    ABSENT = "ABSENT"


class Moisture(Enum):
    MOIST = "MOIST"
    DRY = "DRY"
    WET = "WET"
    STICKY = "STICKY"


class TongueRegion(Enum):
    TIP = "TIP"
    UJ = "UJ"
    MJ = "MJ"
    LJ = "LJ"
    SIDES = "SIDES"


@dataclass
class Tongue:
    body_color: BodyColor = BodyColor.PINK
    body_shapes: List[BodyShape] = BodyShape.REGULAR
    coating_color: CoatingColor = CoatingColor.TRANSPARENT
    coating_thickness: CoatingThickness = CoatingThickness.THIN
    moisture: Moisture = Moisture.MOIST
    region: TongueRegion = None
