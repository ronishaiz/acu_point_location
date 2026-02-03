import os.path
from typing import List, Set, Optional
from dataclasses import dataclass
from enum import Enum

import toml

from backend.enums import Organ
from pages_backend.flashcards.flashcard import FlashCardObject


class Flavor(Enum):
    SPICY = 'SPICY'
    BITTER = 'BITTER'
    SWEET = 'SWEET'
    SALTY = 'SALTY'
    SOUR = 'SOUR'
    AROMATIC = 'AROMATIC'


class Temperature(Enum):
    HOT = 'HOT'
    COLD = 'COLD'
    MILD = 'MILD'


class TemperatureAccent(Enum):
    PLUS_PLUS = "'++'"
    PLUS = "'+'"
    NEUTRAL = ''
    MINUS = "'-'"
    MINUS_MINUS = "'--'"


class HerbGroup(Enum):
    WARM_EXTERIOR_RELEASERS = 'WARM_EXTERIOR_RELEASERS'
    COLD_EXTERIOR_RELEASERS = 'COLD_EXTERIOR_RELEASERS'
    HEAT_PURIFIERS_AND_DAMP_DRYERS = 'HEAT_PURIFIERS_AND_DAMP_DRYERS'
    DOWNWARD_DRAINERS = 'DOWNWARD_DRAINERS'
    FIRE_DRAINERS = 'FIRE_DRAINERS'
    FIRE_AND_TOXIN_RELEASERS = 'FIRE_AND_TOXIN_RELEASERS'
    EMPTY_HEAT_RELEASERS = 'EMPTY_HEAT_RELEASERS'
    DISPEL_SUMMER_HEAT = 'EXPEL_SUMMER_HEAT'
    DRAIN_HUMIDITY_THROUGH_URINATION = 'EXTRACT_HUMIDITY_THROUGH_URINATION'
    AROMATIC_HUMIDITY_TRANSFORMATION = 'AROMATIC_HUMIDITY_TRANSFORMATION'
    AROMATIC_ORIFICE_OPENING = 'AROMATIC_ORIFICE_OPENING'
    DISPEL_WIND_DAMPNESS = 'DISPEL_WIND_DAMPNESS'
    CLEAR_PHLEGM = 'CLEAR_PHLEGM'
    STOP_COUGH = 'STOP_COUGH'
    DISPEL_PHLEGM_BY_VOMITING = 'DISPEL_PHLEGM_BY_VOMITING'
    TONIFY_QI = 'TONIFY_QI'
    TONIFY_YIN = 'TONIFY_YIN'
    TONIFY_YANG = 'TONIFY_YANG'
    HEAT_INTERIOR = 'HEAT_INTERIOR'
    MOVE_QI = 'MOVE_QI'
    MOVE_BLOOD = 'MOVE_BLOOD'
    STOP_BLEEDING = 'STOP_BLEEDING'
    ABSORBERS = 'ABSORBERS'
    CALM_THE_SPIRIT = 'CALM_THE_SPIRIT'
    TOFINY_HEART_FOR_CALMING_THE_SPIRIT = 'TONIFY_HEART_FOR_CALMING_THE_SPIRIT'
    DISPEL_WIND_AND_TREMOR = 'DISPEL_WIND_AND_TREMOR'
    TREAT_FOOD_STAGNATION = 'TREAT_FOOD_STAGNATION'
    DISPEL_PARASITES = 'DISPEL_PARASITES'

@dataclass
class Herb(FlashCardObject):

    _name: str
    _western_name: str = None
    _flavors: List[Flavor] = None
    _temperature: Temperature = None
    _temperature_accent: TemperatureAccent = None
    _counter_indications: List[str] = None
    _functions: List[str] = None
    _herb_group: HerbGroup = None
    _affected_organs: List[Organ] = None
    _use_with: List[str] = None
    _notes: List[str] = None
    _focus_remark: str = None

    @property
    def identifier(self) -> str:
        return self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def flavors(self) -> List[Flavor]:
        return self._flavors or []

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

    @property
    def affected_organs(self) -> List[Organ]:
        return self._affected_organs or []

    @property
    def use_with(self) -> List[str]:
        return self._use_with or []

    @property
    def western_name(self) -> Optional[str]:
        return self._western_name

    @property
    def notes(self) -> List[str]:
        return self._notes or []

    @property
    def focus_remark(self) -> Optional[str]:
        return self._focus_remark

    @classmethod
    def get_property_name_to_flash_card_property_name(cls) -> dict:
        return {
            'name': 'Name',
            'western_name': 'Western Name',
            'flavors': 'Flavors',
            'temperature': 'Temperature',
            'temperature_accent': 'Temperature Accent',
            'herb_group': 'Herb Group',
            'functions': 'Functions',
            'counter_indications': 'Counter Indications',
            'affected_organs': 'Affected Organs',
            'use_with': 'Use With',
            'notes': 'Notes',
            'focus_remark': 'Focus Remark'
        }

    @classmethod
    def from_dict(cls, herb_dict: dict, name: str) -> 'Herb':
        # Parse flavors: accept list or single value; fall back to legacy 'flavor' key
        flavors_val = None
        if 'flavors' in herb_dict and herb_dict['flavors']:
            if isinstance(herb_dict['flavors'], list):
                flavors_val = [Flavor(f) for f in herb_dict['flavors']]
            else:
                flavors_val = [Flavor(herb_dict['flavors'])]
        elif 'flavor' in herb_dict and herb_dict['flavor']:
            # backwards compatibility for single flavor entries
            flavors_val = [Flavor(herb_dict['flavor'])]

        return cls(
            _name=name,
            _western_name=herb_dict.get('western_name', None),
            _flavors=flavors_val,
            _temperature=Temperature(herb_dict['temperature']) if 'temperature' in herb_dict and herb_dict['temperature'] else None,
            _temperature_accent=TemperatureAccent(herb_dict['temperature_accent']) if 'temperature_accent' in herb_dict and herb_dict['temperature_accent'] else None,
            _counter_indications=herb_dict.get('counter_indications', []),
            _functions=herb_dict.get('functions', []),
            _herb_group=HerbGroup(herb_dict['herb_group']) if 'herb_group' in herb_dict and herb_dict['herb_group'] else None,
            _affected_organs=[Organ(org) for org in herb_dict.get('affected_organs', [])],
            _use_with=herb_dict.get('use_with', []),
            _notes=herb_dict.get('notes', []),
            _focus_remark=herb_dict.get('focus_remark', None)
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

def get_available_herb_groups() -> List[HerbGroup]:
    """Return a sorted list of HerbGroup enums that appear in the loaded herbs."""
    groups: Set[HerbGroup] = {herb.herb_group for herb in ALL_HERBS if herb.herb_group is not None}
    return sorted(groups, key=lambda g: g.name)


def get_herb_group_options() -> List[dict]:
    """
    Return a list of dicts suitable for a selectbox/options control:
    [{'label': 'Exterior Releasers', 'value': 'EXTERIOR_RELEASERS'}, ...]
    """
    return [
        {'label': g.name.replace('_', ' ').title(), 'value': g.value}
        for g in get_available_herb_groups()
    ]


def filter_herbs_by_groups(selected_groups: Optional[List[str]] = None) -> List[Herb]:
    """
    Return herbs whose herb_group is in selected_groups.
    selected_groups may be a list of HerbGroup enums, or a list of string values (enum.value).
    If selected_groups is None or empty, all herbs are returned.
    """
    if not selected_groups:
        return ALL_HERBS

    selected_values = {g.value if isinstance(g, HerbGroup) else g for g in selected_groups}
    return [herb for herb in ALL_HERBS if herb.herb_group and herb.herb_group.value in selected_values]
