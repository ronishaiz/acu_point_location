from enum import Enum
from random import shuffle
from typing import TypeVar, Generic, List

T = TypeVar("T")


class Queue(Generic[T]):

    def __init__(self, elements: List[T], sort: bool = False):

        if not sort:
            shuffle(elements)

        self._elements = elements

    def get_top(self) -> T:
        return self._elements[0]

    def prev(self) -> None:
        self._elements = [self._elements[-1]] + self._elements[:-1]

    def next(self) -> None:
        self._elements = self._elements[1:] + [self._elements[0]]

    @property
    def empty(self) -> bool:
        return not self._elements


def format_displayable_object(displayable_object: object):
    new_displayable_object = displayable_object

    if isinstance(displayable_object, Enum):
        new_displayable_object = str(displayable_object.value)

    if isinstance(displayable_object, list):

        new_displayable_object = []
        for item in displayable_object:

            if isinstance(item, Enum):
                item = str(item.value)
                new_displayable_object.append(item)

            else:
                new_displayable_object.append(item)

    return new_displayable_object
