#!/usr/bin/env python

from collections import OrderedDict
from .element import Element


class ElementCollection(OrderedDict):
    def __init__(self):
        super().__init__()
        self._last_id = -1

    @property
    def last_id(self) -> int:
        return self._last_id

    @last_id.setter
    def last_id(self, id_: int) -> None:
        self._last_id = id_

    def add(self, element: Element) -> None:
        self.last_id += 1
        self.__setitem__(self.last_id, element)
        element.id = self.last_id  # Auto-update on element add
