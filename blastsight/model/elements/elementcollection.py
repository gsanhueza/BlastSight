#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from collections import OrderedDict
from .element import Element


class ElementCollection(OrderedDict):
    def __init__(self):
        super().__init__()
        self.current_id = -1

    @property
    def last_id(self):
        # bool(dict) evaluates to False if the dictionary is empty
        return list(self.keys())[-1] if bool(self) else -1

    def add(self, element: Element) -> None:
        self.current_id += 1
        self[self.current_id] = element
        element.id = self.current_id  # Auto-update on element add

    def delete(self, _id):
        del self[_id]
