
import os.path
from typing import List
from dataclasses import dataclass
from enum import Enum

import toml

from pages_backend.flashcards.flashcard import FlashCardObject


class Flavor(Enum):
    SPICY: str = 'SPICY'
    BITTER: str = 'BITTER'
    SWEET: str = 'SWEET'
    SALTY: str = 'SALTY'
    SOUR: str = 'SOUR'


class Temperature(Enum):
    HOT: str = 'HOT'
    COLD: str = 'COLD'
    MILD: str = 'MILD'


class TemperatureAccent(Enum):
    PLUS_PLUS: str = '++'
    PLUS: str = '+'
    NEUTRAL: str = ''
    MINUS: str = '-'
    MINUS_MINUS: str = '--'


class HerbGroup(Enum):
    RELEASE_THE_EXTERIOR: str = 'RELEASE_THE_EXTERIOR'
    CLEAR_HEAT_AND_DRY_HUMIDITY: str = 'CLEAR_HEAT_AND_DRY_HUMIDITY'
    DRAIN_DOWNWARDS: str = 'DRAIN_DOWNWARDS'
    DISPEL_FIRE: str = 'EXPEL_FIRE'
    DISPEL_FIRE_AND_TOXINS: str = 'EXPEL_FIRE_AND_TOXINS'
    DISPEL_SUMMER_HEAT: str = 'EXPEL_SUMMER_HEAT'
    DRAIN_HUMIDITY_THROUGH_URINATION: str = 'EXTRACT_HUMIDITY_THROUGH_URINATION'
    AROMATIC_HUMIDITY_TRANSFORMATION: str = 'AROMATIC_HUMIDITY_TRANSFORMATION'
    AROMATIC_ORIFICE_OPENING: str = 'AROMATIC_ORIFICE_OPENING'
    DISPEL_WIND_DAMPNESS: str = 'DISPEL_WIND_DAMPNESS'
    CLEAR_PHLEGM: str = 'CLEAR_PHLEGM'
    STOP_COUGH: str = 'STOP_COUGH'
    DISPEL_PHLEGM_BY_VOMITING: str = 'DISPEL_PHLEGM_BY_VOMITING'
    TONIFY_QI: str = 'TONIFY_QI'
    TONIFY_YIN: str = 'TONIFY_YIN'
    TONIFY_YANG: str = 'TONIFY_YANG'
    HEAT_INTERIOR: str = 'HEAT_INTERIOR'
    MOVE_QI: str = 'MOVE_QI'
    MOVE_BLOOD: str = 'MOVE_BLOOD'
    STOP_BLEEDING: str = 'STOP_BLEEDING'
    ABSORBERS: str = 'ABSORBERS'
    CALM_THE_SPIRIT: str = 'CALM_THE_SPIRIT'
    TOFINY_HEART_FOR_CALMING_THE_SPIRIT: str = 'TONIFY_HEART_FOR_CALMING_THE_SPIRIT'
    DISPEL_WIND_AND_TREMOR: str = 'DISPEL_WIND_AND_TREMOR'
    TREAT_FOOD_STAGNATION: str = 'TREAT_FOOD_STAGNATION'
    DISPEL_PARASITES: str = 'DISPEL_PARASITES'

@dataclass
class Herb(FlashCardObject):

    _name: str
    _flavor: Flavor = None
    _temperature: Temperature = None
    _temperature_accent: TemperatureAccent = None
    _counter_indications: List[str] = None
    _functions: List[str] = None
    _herb_group: HerbGroup = None

    @property
    def identifier(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def flavor(self) -> Flavor:
        return self._flavor

    @property
    def temperature(self) -> Temperature:
        return self._temperature

    @property
    def temperature_accent(self) -> TemperatureAccent:
        return self._temperature_accent

    @property
    def counter_indications(self) -> List[str]:
        return self._counter_indications or []

    @property
    def functions(self) -> List[str]:
        return self._functions or []

    @property
    def herb_group(self) -> HerbGroup:
        return self._herb_group

    @classmethod
    def get_property_name_to_flash_card_property_name(cls) -> dict:
        return {
            'name': 'Name',
            'flavor': 'Flavor',
            'temperature': 'Temperature',
            'temperature_accent': 'Temperature Accent',
            'herb_group': 'Herb Group',
            'functions': 'Functions',
            'counter_indications': 'Counter Indications'
        }

    @classmethod
    def from_dict(cls, herb_dict: dict, name: str) -> 'Herb':
        return cls(
            _name=name,
            _flavor=Flavor(herb_dict['flavor']) if 'flavor' in herb_dict and herb_dict['flavor'] else None,
            _temperature=Temperature(herb_dict['temperature']) if 'temperature' in herb_dict and herb_dict['temperature'] else None,
            _temperature_accent=TemperatureAccent(herb_dict['temperature_accent']) if 'temperature_accent' in herb_dict and herb_dict['temperature_accent'] else None,
            _counter_indications=herb_dict.get('counter_indications', []),
            _functions=herb_dict.get('functions', []),
            _herb_group=HerbGroup(herb_dict['herb_group']) if 'herb_group' in herb_dict and herb_dict['herb_group'] else None
        )

    @classmethod
    def from_toml(cls, toml_file_path: str) -> List['Herb']:
        with open(toml_file_path, 'r') as f:
            herbs_dict = toml.load(f)

        return [cls.from_dict(herb_dict, name) for name, herb_dict in herbs_dict.items()]


def load_all_herbs() -> List[Herb]:
    """Load all herbs from TOML files in the data directory."""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    all_herbs = []
    
    if not os.path.exists(data_dir):
        return all_herbs
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.toml'):
            file_path = os.path.join(data_dir, filename)
            herbs = Herb.from_toml(file_path)
            all_herbs.extend(herbs)
    
    return all_herbs


def get_herb_by_name(name: str) -> Herb:
    """Get a herb by its name."""
    for herb in ALL_HERBS:
        if herb.name == name:
            return herb
    raise ValueError(f"Herb with name '{name}' not found")


ALL_HERBS = load_all_herbs()
