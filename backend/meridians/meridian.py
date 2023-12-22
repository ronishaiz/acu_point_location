import os.path
from dataclasses import dataclass
from typing import List

import toml

from backend.enums import Organ, Stage, Element, Limb
from backend.points.point import Point
from pages_backend.flashcards.flashcard import FlashCardObject


@dataclass
class Meridian(FlashCardObject):

    _stage: Stage = None
    _organ: Organ = None
    _element: Element = None
    _limb: Limb = None

    _yin_yang_partner_organ: Organ = None
    _stage_partner_organ: Organ = None

    _hours: tuple = None

    _points: List[Point] = None

    _number_of_learned_points: int = None

    @property
    def identifier(self):
        return self.limb.value + f" {self.stage.value}"

    @property
    def stage(self) -> Stage:
        return self._stage

    @property
    def organ(self) -> Organ:
        return self._organ

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

    @property
    def points(self) -> List[Point]:
        return self._points

    @property
    def number_of_learned_points(self) -> int:
        return self._number_of_learned_points

    @classmethod
    def get_property_name_to_flash_card_property_name(cls) -> dict:
        return {'organ': 'Organ',
                'stage': 'Stage',
                'element': 'Element',
                'limb': 'Limb',
                'yin_yang_partner_organ': 'Partner in Yin-Yang Relationship',
                'stage_partner_organ': 'Partner in Same Stage',
                'hours': 'Hours'}

    def __post_init__(self):
        self._points = self._get_points()

    def _get_points(self) -> List[Point]:
        path_to_toml = os.path.join(os.path.dirname(__file__), 'data', self.organ.value + '.toml')

        with open(path_to_toml, 'r') as f:
            points_dict = toml.load(f)

        return [Point.get_point_from_dict(point_dict, identifier) for identifier, point_dict in points_dict.items()]


LU_MERIDIAN = Meridian(_stage=Stage.tai_yin, _organ=Organ.LU, _element=Element.METAL, _limb=Limb.HAND,
                       _yin_yang_partner_organ=Organ.LI, _stage_partner_organ=Organ.SP, _hours=(3, 5),
                       _number_of_learned_points=9)

# LI_MERIDIAN = Meridian(stage=Stage.yang_ming, organ=Organ.LI, element=Element.METAL, limb=Limb.LEG,
#                        yin_yang_partner_organ=Organ.LU, stage_partner_organ=Organ.ST, hours=(5, 7))


ALL_MERIDIANS = [LU_MERIDIAN]
ALL_POINTS = [item for sublist in [meridian.points for meridian in ALL_MERIDIANS] for item in sublist]
