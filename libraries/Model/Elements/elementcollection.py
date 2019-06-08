#!/usr/bin/env python

from collections import OrderedDict
from .element import Element


class ElementCollection(OrderedDict):
    def __init__(self):
        super().__init__()
        self.last_id = -1

    def add(self, element: Element) -> None:
        self.last_id += 1
        self.__setitem__(self.last_id, element)
        element.id = self.last_id  # Auto-update on element add
