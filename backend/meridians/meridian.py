import os.path
import re
from abc import ABCMeta
from dataclasses import dataclass
from typing import List

import toml

from backend.enums import MeridianName, Stage, Element, Limb, Organ
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

    _yin_yang_partner_organ: Organ = None
    _stage_partner_organ: Organ = None

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
    def yin_yang_partner_organ(self) -> Organ:
        return self._yin_yang_partner_organ

    @property
    def stage_partner_organ(self) -> Organ:
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
                             _yin_yang_partner_organ=Organ.LI, _stage_partner_organ=Organ.SP, _hours=(3, 5),
                             _number_of_learned_points=9)

LI_MERIDIAN = ZangFuMeridian(_stage=Stage.yang_ming, _name=MeridianName.LI, _element=Element.METAL, _limb=Limb.LEG,
                             _yin_yang_partner_organ=Organ.LU, _stage_partner_organ=Organ.ST, _hours=(5, 7),
                             _number_of_learned_points=12)

CV_MERIDIAN = SpecialMeridian(_name=MeridianName.CV, _number_of_learned_points=17, _opening_point='LU7', _closing_point='KID6',
                              _region='Front', _yin_yang='Yin')

ST_MERIDIAN = ZangFuMeridian(_stage=Stage.yang_ming, _name=MeridianName.ST, _element=Element.EARTH, _limb=Limb.LEG,
                             _yin_yang_partner_organ=Organ.SP, _stage_partner_organ=Organ.LI, _hours=(7, 9),
                             _number_of_learned_points=28)

SP_MERIDIAN = ZangFuMeridian(_stage=Stage.tai_yin, _name=MeridianName.SP, _element=Element.EARTH, _limb=Limb.LEG,
                             _yin_yang_partner_organ=Organ.ST, _stage_partner_organ=Organ.LU, _hours=(9, 11),
                             _number_of_learned_points=11)

HT_MERIDIAN = ZangFuMeridian(_stage=Stage.shao_yin, _name=MeridianName.HT, _element=Element.FIRE, _limb=Limb.HAND,
                             _yin_yang_partner_organ=Organ.SI, _stage_partner_organ=Organ.KID, _hours=(11, 13),
                             _number_of_learned_points=8)

SI_MERIDIAN = ZangFuMeridian(_stage=Stage.tai_yang, _name=MeridianName.SI, _element=Element.FIRE, _limb=Limb.HAND,
                             _yin_yang_partner_organ=Organ.HT, _stage_partner_organ=Organ.BL, _hours=(13, 15),
                             _number_of_learned_points=17)

GV_MERIDIAN = SpecialMeridian(_name=MeridianName.GV, _number_of_learned_points=14, _opening_point='SI3', _closing_point='BL62',
                              _region='Back', _yin_yang='Yang')

BL_MERIDIAN = ZangFuMeridian(_stage=Stage.tai_yang, _name=MeridianName.BL, _element=Element.WATER, _limb=Limb.LEG,
                             _yin_yang_partner_organ=Organ.KID, _stage_partner_organ=Organ.SI, _hours=(15, 17),
                             _number_of_learned_points=43)


def get_meridian_by_name(name: MeridianName):
    if name == MeridianName.LU:
        return LU_MERIDIAN

    elif name == MeridianName.LI:
        return LI_MERIDIAN

    elif name == MeridianName.CV:
        return CV_MERIDIAN

    elif name == MeridianName.ST:
        return ST_MERIDIAN

    elif name == MeridianName.SP:
        return SP_MERIDIAN

    elif name == MeridianName.HT:
        return HT_MERIDIAN

    elif name == MeridianName.SI:
        return SI_MERIDIAN

    elif name == MeridianName.GV:
        return GV_MERIDIAN

    elif name == MeridianName.BL:
        return BL_MERIDIAN

    else:
        raise Exception("Non supported meridian")


def get_point_by_identifier(identifier: str) -> Point:
    matched = re.match('([A-Z]*)([0-9]*)', identifier)
    meridian_name = matched.group(1)

    meridian = get_meridian_by_name(MeridianName(meridian_name))
    possible_points = [point for point in meridian.points if identifier == point.identifier]

    if len(possible_points) != 1:
        raise ValueError(f"Could not find the point with the identifier: {identifier} in the meridian: {meridian.name.value}")

    return possible_points[0]


ALL_MERIDIANS = [LU_MERIDIAN, LI_MERIDIAN, CV_MERIDIAN, ST_MERIDIAN, SP_MERIDIAN, HT_MERIDIAN, SI_MERIDIAN, GV_MERIDIAN, BL_MERIDIAN]
ALL_POINTS = [item for sublist in [meridian.points for meridian in ALL_MERIDIANS] for item in sublist]
