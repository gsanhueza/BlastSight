#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .parser import Parser


class ParserCollection:
    def __init__(self):
        self._collection = {}

    def add(self, extension: str, handler: Parser) -> None:
        self._collection[extension] = handler

    def get(self, extension: str) -> Parser:
        return self._collection.get(extension)

    def delete(self, extension: str) -> None:
        del self._collection[extension]
