#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from collections import OrderedDict
from .element import Element


class ElementCollection:
    def __init__(self):
        self._collection = OrderedDict()
        self._current_id = -1

    @property
    def last_id(self) -> int:
        # bool(dict) evaluates to False if the dictionary is empty
        return list(self._collection.keys())[-1] if bool(self._collection) else -1

    def add(self, element: Element) -> None:
        if element.id == -1:  # Automatic ID
            self._current_id += 1
            self._collection[self._current_id] = element
            element.id = self._current_id  # Auto-update on element add
        else:  # Manual ID
            self._collection[element.id] = element

    def get(self, _id: int) -> Element:
        return self._collection.get(_id)

    def size(self) -> int:
        return len(self._collection)

    def delete(self, _id: int) -> None:
        del self._collection[_id]
        if self.size() == 0:
            self._current_id = -1

    def clear(self) -> None:
        self._collection.clear()
        self._current_id = -1
