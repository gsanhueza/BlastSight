#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from collections import OrderedDict


class GLProgramCollection:
    def __init__(self):
        self._collection = OrderedDict()

    def associate(self, program_type, association) -> None:
        self._collection[program_type] = association

    def get_programs(self) -> dict.keys:
        return self._collection.keys()

    def get_associations(self) -> dict.values:
        return self._collection.values()

    def get_pairs(self) -> dict.items:
        return self._collection.items()
