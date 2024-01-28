import os.path
from abc import ABCMeta
from dataclasses import dataclass
from typing import List

import toml

from backend.enums import MeridianName, Stage, Element, Limb
from backend.points.point import Point
from pages_backend.flashcards.flashcard import FlashCardObject


@dataclass
class MeridianBase(FlashCardObject, metaclass=ABCMeta):
    _name: MeridianName = None

    _points: List[Point] = None

    _number_of_learned_points: int = None

    def __post_init__(self):
        self._points = self._get_points()

    @property
    def number_of_learned_points(self) -> int:
        return self._number_of_learned_points

    @property
    def name(self) -> MeridianName:
        return self._name

    @property
    def points(self) -> List[Point]:
        return self._points

    def _get_points(self) -> List[Point]:
        path_to_toml = os.path.join(os.path.dirname(__file__), 'data', self.name.value + '.toml')

        with open(path_to_toml, 'r') as f:
            points_dict = toml.load(f)

        return [Point.get_point_from_dict(point_dict, identifier) for identifier, point_dict in points_dict.items()]


@dataclass
class ZangFuMeridian(MeridianBase):
    _stage: Stage = None
    _name: MeridianName = None
    _element: Element = None
    _limb: Limb = None

    _yin_yang_partner_organ: MeridianName = None
    _stage_partner_organ: MeridianName = None

    _hours: tuple = None

    @property
    def identifier(self):
        return self.limb.value + f" {self.stage.value}"

    @property
    def stage(self) -> Stage:
        return self._stage

    @property
    def element(self) -> Element:
        return self._element

    @property
    def limb(self) -> Limb:
        return self._limb

    @property
    def yin_yang_partner_organ(self) -> MeridianName:
        return self._yin_yang_partner_organ

    @property
    def stage_partner_organ(self) -> MeridianName:
        return self._stage_partner_organ

    @property
    def hours(self) -> tuple:
        return self._hours

    @classmethod
    def get_property_name_to_flash_card_property_name(cls) -> dict:
        return {'name': 'Organ',
                'stage': 'Stage',
                'element': 'Element',
                'limb': 'Limb',
                'yin_yang_partner_organ': 'Partner in Yin-Yang Relationship',
                'stage_partner_organ': 'Partner in Same Stage',
                'hours': 'Hours'}


@dataclass
class SpecialMeridian(MeridianBase):

    _opening_point: str = None
    _closing_point: str = None
    _region: str = None
    _yin_yang: str = None

    @property
    def identifier(self):
        return self.name

    @property
    def opening_point(self):
        return self._opening_point

    @property
    def closing_point(self):
        return self._closing_point

    @property
    def region(self):
        return self._region

    @property
    def yin_yang(self):
        return self._yin_yang

    @classmethod
    def get_property_name_to_flash_card_property_name(cls) -> dict:
        return {'name': 'Name',
                'opening_point': 'Opening Point',
                'closing_point': 'Closing Point',
                'region': 'Region',
                'yin_yang': 'Yin Yang'}


LU_MERIDIAN = ZangFuMeridian(_stage=Stage.tai_yin, _name=MeridianName.LU, _element=Element.METAL, _limb=Limb.HAND,
                             _yin_yang_partner_organ=MeridianName.LI, _stage_partner_organ=MeridianName.SP, _hours=(3, 5),
                             _number_of_learned_points=9)

LI_MERIDIAN = ZangFuMeridian(_stage=Stage.yang_ming, _name=MeridianName.LI, _element=Element.METAL, _limb=Limb.LEG,
                             _yin_yang_partner_organ=MeridianName.LU, _stage_partner_organ=MeridianName.ST, _hours=(5, 7),
                             _number_of_learned_points=12)

CV_MERIDIAN = SpecialMeridian(_name=MeridianName.CV, _number_of_learned_points=17, _opening_point='LU7', _closing_point='KID6',
                              _region='Front', _yin_yang='Yin')

ST_MERIDIAN = ZangFuMeridian(_stage=Stage.yang_ming, _name=MeridianName.ST, _element=Element.EARTH, _limb=Limb.LEG,
                             _yin_yang_partner_organ=MeridianName.SP, _stage_partner_organ=MeridianName.LI, _hours=(7, 9),
                             _number_of_learned_points=16)


def get_meridian_by_name(name: MeridianName):
    if name == MeridianName.LU:
        return LU_MERIDIAN

    elif name == MeridianName.LI:
        return LI_MERIDIAN

    elif name == MeridianName.CV:
        return CV_MERIDIAN

    elif name == MeridianName.ST:
        return ST_MERIDIAN

    else:
        raise Exception("Non supported meridian")


ALL_MERIDIANS = [LU_MERIDIAN, LI_MERIDIAN, CV_MERIDIAN, ST_MERIDIAN]
ALL_POINTS = [item for sublist in [meridian.points for meridian in ALL_MERIDIANS] for item in sublist]
