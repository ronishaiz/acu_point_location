from enum import Enum
import os.path
from typing import List, Union
from dataclasses import dataclass

import toml

from backend.diagnosis.eight_principles import EightPrinciples, InternalExternalPrinciple, FullEmptyPrinciple, HotColdPrinciple, YinYangPrinciple
from backend.diagnosis.pulse import Pulse, Speed, Depth, Strength, Quality, PulsePosition, PositionYinYang, PositionJiao, PositionHand
from backend.diagnosis.tongue import Tongue, BodyColor, BodyShape, CoatingColor, CoatingThickness, Moisture, TongueRegion
from backend.enums import Organ
from backend.herbs.herb import Herb, get_herb_by_name
from backend.meridians.meridian import get_point_by_identifier
from backend.points.point import Point
from pages_backend.flashcards.flashcard import FlashCardObject


class AcupunctureTechnique(Enum):
    TONFIY = "TONIFY"
    SEDATE = "SEDATE"
    MOXA = "MOXA"
    

@dataclass
class Treatment:
    _principle: str
    _points: List[Union[Point, str]] = None
    _acupuncture_techniques: List[AcupunctureTechnique] = None
    _nutrition: List[str] = None
    _herbs: List[Union[Herb, str]] = None

    @property
    def points(self) -> List[Point]:
        return self._points or []

    @property
    def nutrition(self) -> List[str]:
        return self._nutrition or []

    @property
    def herbs(self) -> List[Union[Herb, str]]:
        return self._herbs or []

    @property
    def acupuncture_techniques(self) -> List[AcupunctureTechnique]:
        return self._acupuncture_techniques or []

    @property
    def principle(self) -> str:
        return self._principle

    @classmethod
    def from_dict(cls, d: dict) -> 'Treatment':
        points = []
        if 'points' in d:
            points = [cls._get_point_or_str(point_id) for point_id in d['points']]
        
        herbs = []
        if 'herbs' in d:
            for herb_name in d['herbs']:
                try:
                    herbs.append(get_herb_by_name(herb_name))
                except ValueError:
                    # If herb not found, store as string (non-clickable)
                    herbs.append(herb_name)
        
        acupuncture_techniques = []
        if 'acupuncture_techniques' in d:
            acupuncture_techniques = [AcupunctureTechnique(tech) for tech in d['acupuncture_techniques']]
        
        return cls(
            _principle=d.get('principle', ''),
            _points=points,
            _nutrition=d.get('nutrition', []),
            _herbs=herbs,
            _acupuncture_techniques=acupuncture_techniques
        )

    @classmethod
    def _get_point_or_str(cls, point_str: str) -> str:
        try:
            return get_point_by_identifier(point_str)
        except ValueError as e:
            return point_str


@dataclass
class Diagnosis:
    _pulse: Pulse = None
    _tongue: Tongue = None
    _symptoms: List[str] = None
    _key_symptoms: List[str] = None
    _eight_principles: EightPrinciples = None

    @property
    def pulse(self) -> Pulse:
        return self._pulse

    @property
    def tongue(self) -> Tongue:
        return self._tongue

    @property
    def symptoms(self) -> List[str]:
        return self._symptoms or []

    @property
    def key_symptoms(self) -> List[str]:
        return self._key_symptoms or []

    @property
    def eight_principles(self) -> EightPrinciples:
        return self._eight_principles

    @classmethod
    def from_dict(cls, d: dict) -> 'Diagnosis':
        pulse = None
        if 'pulse' in d:
            pulse_dict = d['pulse']
            positions = []
            if 'positions' in pulse_dict:
                for pos_dict in pulse_dict['positions']:
                    if 'yin_yang' in pos_dict and 'jiao' in pos_dict and 'left_right' in pos_dict:
                        positions.append(PulsePosition(
                            yin_yang=PositionYinYang(pos_dict['yin_yang']),
                            jiao=PositionJiao(pos_dict['jiao']),
                            left_right=PositionHand(pos_dict['left_right'])
                        ))
            qualities = []
            if 'quality' in pulse_dict:
                quality_data = pulse_dict['quality']
                # Handle both single value (for backward compatibility) and list
                if isinstance(quality_data, list):
                    qualities = [Quality(q) for q in quality_data]
                else:
                    qualities = [Quality(quality_data)]
            
            pulse = Pulse(
                _speed=Speed(pulse_dict['speed']) if 'speed' in pulse_dict else None,
                _depth=Depth(pulse_dict['depth']) if 'depth' in pulse_dict else None,
                _strength=Strength(pulse_dict['strength']) if 'strength' in pulse_dict else None,
                _quality=qualities,
                _positions=positions
            )

        tongue = None
        if 'tongue' in d:
            tongue_dict = d['tongue']
            tongue = Tongue(
                body_color=BodyColor(tongue_dict['body_color']) if 'body_color' in tongue_dict else None,
                body_shapes=[BodyShape(shape) for shape in tongue_dict.get('body_shapes', [])],
                coating_color=CoatingColor(tongue_dict['coating_color']) if 'coating_color' in tongue_dict else None,
                coating_thickness=CoatingThickness(tongue_dict['coating_thickness']) if 'coating_thickness' in tongue_dict else None,
                moisture=Moisture(tongue_dict['moisture']) if 'moisture' in tongue_dict else None,
                region=TongueRegion(tongue_dict['region']) if 'region' in tongue_dict else None
            )

        eight_principles = None
        if 'eight_principles' in d:
            ep_dict = d['eight_principles']
            eight_principles = EightPrinciples()
            if 'internal_external' in ep_dict:
                eight_principles.intenal_external = InternalExternalPrinciple(ep_dict['internal_external'])
            if 'full_empty' in ep_dict:
                eight_principles.full_empty = FullEmptyPrinciple(ep_dict['full_empty'])
            if 'hot_cold' in ep_dict:
                eight_principles.hot_cold = HotColdPrinciple(ep_dict['hot_cold'])
            if 'yin_yang' in ep_dict:
                eight_principles.yin_yang = YinYangPrinciple(ep_dict['yin_yang'])

        symptoms = d.get('symptoms', [])
        key_symptoms = d.get('key_symptoms', [])

        return cls(
            _pulse=pulse,
            _tongue=tongue,
            _symptoms=symptoms,
            _key_symptoms=key_symptoms,
            _eight_principles=eight_principles
        )


@dataclass
class Syndrome(FlashCardObject):
    _name: str
    _organ: Organ
    _diagnosis: Diagnosis
    _treatment: Treatment
    _ethiology: List[str] = None

    @property
    def identifier(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def organ(self) -> Organ:
        return self._organ

    @property
    def diagnosis(self) -> Diagnosis:
        return self._diagnosis

    @property
    def treatment(self) -> Treatment:
        return self._treatment

    @property
    def ethiology(self) -> List[str]:
        return self._ethiology or []

    @property
    def diagnosis_str(self) -> str:
        """Format diagnosis as a readable string."""
        parts = []
        if self._diagnosis.symptoms:
            symptoms_str = "* " + '\n* '.join(self._diagnosis.symptoms)
            if self._diagnosis.key_symptoms:
                # Highlight key symptoms
                key_symptoms_str = "* " + '\n* '.join(self._diagnosis.key_symptoms)
                parts.append(f"Symptoms:\n{symptoms_str}\n")
                parts.append(f"Key Symptoms:\n{key_symptoms_str}\n")
            else:
                parts.append(f"Symptoms:\n{symptoms_str}\n")
        if self._diagnosis.pulse:
            pulse_parts = []
            if self._diagnosis.pulse._speed:
                pulse_parts.append(f"Speed: {self._diagnosis.pulse._speed.value}\n")
            if self._diagnosis.pulse._depth:
                pulse_parts.append(f"Depth: {self._diagnosis.pulse._depth.value}\n")
            if self._diagnosis.pulse._strength:
                pulse_parts.append(f"Strength: {self._diagnosis.pulse._strength.value}\n")
            if self._diagnosis.pulse._quality:
                quality_values = ', '.join([q.value for q in self._diagnosis.pulse._quality])
                pulse_parts.append(f"Quality: {quality_values}\n")
            if self._diagnosis.pulse._positions:
                position_strs = []
                for pos in self._diagnosis.pulse._positions:
                    pos_parts = []
                    if pos.yin_yang:
                        pos_parts.append(pos.yin_yang.value)
                    if pos.jiao:
                        pos_parts.append(pos.jiao.value)
                    if pos.left_right:
                        pos_parts.append(pos.left_right.value)
                    if pos_parts:
                        position_strs.append('/'.join(pos_parts))
                if position_strs:
                    pulse_parts.append(f"Positions: {', '.join(position_strs)}\n")
            if pulse_parts:
                parts.append(f"Pulse:\n")
                parts.append(f"{', '.join(pulse_parts)}\n")
        if self._diagnosis.tongue:
            tongue_parts = []
            if self._diagnosis.tongue.body_color:
                tongue_parts.append(f"Body Color: {self._diagnosis.tongue.body_color.value}\n")
            if self._diagnosis.tongue.body_shapes:
                tongue_parts.append(f"Body Shapes: {', '.join([s.value for s in self._diagnosis.tongue.body_shapes])}\n")
            if self._diagnosis.tongue.coating_color:
                tongue_parts.append(f"Coating Color: {self._diagnosis.tongue.coating_color.value}\n")
            if self._diagnosis.tongue.coating_thickness:
                tongue_parts.append(f"Coating Thickness: {self._diagnosis.tongue.coating_thickness.value}\n")
            if self._diagnosis.tongue.moisture:
                tongue_parts.append(f"Moisture: {self._diagnosis.tongue.moisture.value}\n")
            if self._diagnosis.tongue.region:
                tongue_parts.append(f"Region: {self._diagnosis.tongue.region.value}\n")
            if tongue_parts:
                parts.append(f"Tongue:\n")
                parts.append(f"{', '.join(tongue_parts)}\n")
        if self._diagnosis.eight_principles:
            ep_parts = []
            if self._diagnosis.eight_principles.intenal_external:
                ep_parts.append(f"{self._diagnosis.eight_principles.intenal_external.value}\n")
            if self._diagnosis.eight_principles.full_empty:
                ep_parts.append(f"{self._diagnosis.eight_principles.full_empty.value}\n")
            if self._diagnosis.eight_principles.hot_cold:
                ep_parts.append(f"{self._diagnosis.eight_principles.hot_cold.value}\n")
            if self._diagnosis.eight_principles.yin_yang:
                ep_parts.append(f"{self._diagnosis.eight_principles.yin_yang.value}\n")
            if ep_parts:
                parts.append(f"Eight Principles:\n")
                parts.append(f"{', '.join(ep_parts)}\n")
        return "\n".join(parts) if parts else "No diagnosis information available"

    @property
    def treatment_str(self) -> str:
        """Format treatment as a readable string (without clickable herbs)."""
        parts = []
        if self._treatment.principle:
            parts.append(f"Principle: {self._treatment.principle}")
        if self._treatment.points:
            parts.append(f"Points: {', '.join([p.identifier if isinstance(p, Point) else p for p in self._treatment.points])}")
        if self._treatment.acupuncture_techniques:
            parts.append(f"Acupuncture Techniques: {', '.join([t.value for t in self._treatment.acupuncture_techniques])}")
        if self._treatment.nutrition:
            parts.append(f"Nutrition: {', '.join(self._treatment.nutrition)}")
        if self._treatment.herbs:
            herb_names = [h.name if isinstance(h, Herb) else h for h in self._treatment.herbs]
            parts.append(f"Herbs: {', '.join(herb_names)}")
        return "\n".join(parts) if parts else "No treatment information available"

    @property
    def ethiology_str(self) -> str:
        """Format ethiology as a readable string."""
        if self._ethiology:
            return "* " + '\n* '.join(self._ethiology)
        return "No ethiology information available"

    @classmethod
    def get_property_name_to_flash_card_property_name(cls) -> dict:
        return {
            'name': 'Name',
            'organ': 'Organ',
            'ethiology_str': 'Ethiology',
            'diagnosis_str': 'Diagnosis',
            'treatment_str': 'Treatment'
        }

    @classmethod
    def from_dict(cls, syndrome_dict: dict, name: str) -> 'Syndrome':
        return cls(
            _name=name,
            _organ=Organ(syndrome_dict['organ']),
            _diagnosis=Diagnosis.from_dict(syndrome_dict.get('diagnosis', {})),
            _treatment=Treatment.from_dict(syndrome_dict.get('treatment', {})),
            _ethiology=syndrome_dict.get('ethiology', [])
        )

    @classmethod
    def from_toml(cls, toml_file_path: str) -> List['Syndrome']:
        with open(toml_file_path, 'r') as f:
            syndromes_dict = toml.load(f)

        return [cls.from_dict(syndrome_dict, name) for name, syndrome_dict in syndromes_dict.items()]


def load_all_syndromes() -> List[Syndrome]:
    """Load all syndromes from TOML files in the data directory."""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    all_syndromes = []
    
    if not os.path.exists(data_dir):
        return all_syndromes
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.toml'):
            file_path = os.path.join(data_dir, filename)
            syndromes = Syndrome.from_toml(file_path)
            all_syndromes.extend(syndromes)
    
    return all_syndromes


ALL_SYNDROMES = load_all_syndromes()
