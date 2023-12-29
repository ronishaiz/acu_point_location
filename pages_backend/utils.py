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
