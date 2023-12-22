from dataclasses import dataclass
from typing import List

from backend.enums import PointCharacter, Element
from pages_backend.flashcards.flashcard import FlashCardObject


@dataclass
class Point(FlashCardObject):

    _identifier: str
    _chinese_name: str
    _number: int

    _characters: List[str]
    _location: str
    _find_anatomically: bool
    _functions: List[str]
    _indications: List[str]

    _element: str = None
    _use_with: List[str] = None
    _comments: str = None
    _poem: str = None

    @property
    def identifier(self):
        return self._identifier

    @property
    def chinese_name(self) -> str:
        return self._chinese_name

    @property
    def number(self) -> int:
        return self._number

    @property
    def characters(self) -> List[PointCharacter]:
        return [PointCharacter(character) for character in self._characters]

    @property
    def element(self) -> Element:
        if self._element is None:
            return None  # noqa: OK to return None element

        return Element(self._element)

    @property
    def location(self) -> str:
        return self._location

    @property
    def find_anatomically(self) -> bool:
        return self._find_anatomically

    @property
    def functions(self) -> List[str]:
        return self._functions

    @property
    def indications(self) -> List[str]:
        return self._indications

    @property
    def use_with(self) -> List[str]:
        return self._use_with

    @property
    def comments(self) -> str:
        return self._comments

    @property
    def poem(self) -> List[str]:
        if not self._poem:
            return None  # noqa: OK to return None poem

        return self._poem.split('\n')

    @classmethod
    def get_point_from_dict(cls, point_dict: dict, identifier: str) -> 'Point':
        required_keys = ['chinese_name', 'number', 'characters', 'location', 'find_anatomically', 'functions', 'indications']
        bonus_keys = ['element', 'use_with', 'comments', 'poem']

        missing_required_keys = set(required_keys) - set(point_dict)
        unknown_keys = set(point_dict) - set(required_keys) - set(bonus_keys)

        if missing_required_keys:
            raise ValueError(f"Could not find the following required keys in the point dictionary: "
                             f"{missing_required_keys}")

        if unknown_keys:
            raise ValueError(f"Found the following unknown keys in the point dictionary: {unknown_keys}")

        return cls(_identifier=identifier,
                   _chinese_name=point_dict['chinese_name'],
                   _number=point_dict['number'],
                   _characters=point_dict['characters'],
                   _location=point_dict['location'],
                   _functions=point_dict['functions'],
                   _indications=point_dict['indications'],
                   _find_anatomically=point_dict['find_anatomically'],
                   _element=point_dict.get('element', None),  # noqa: ok to set string as None
                   _use_with=point_dict.get('use_with', None),  # noqa: ok to set string as None
                   _comments=point_dict.get('comments', None),  # noqa: ok to set string as None
                   _poem=point_dict.get('poem', None))  # noqa: ok to set string as None

    @classmethod
    def get_property_name_to_flash_card_property_name(cls) -> dict:
        return {'chinese_name': 'Chinese Name',
                'characters': 'Characters',
                'element': 'Element',
                'location': 'Location',
                'find_anatomically': 'Should Find Anatomically?',
                'functions': 'Functions',
                'indications': 'Indications',
                'use_with': 'Use With',
                'comments': 'Comments',
                'poem': 'Poem'}
