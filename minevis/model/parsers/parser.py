#!/usr/bin/env python

from .parserdata import ParserData


class Parser:
    @staticmethod
    def load_file(path: str) -> ParserData:
        raise NotImplementedError

    @staticmethod
    def save_file(path: str, *args, **kwargs) -> None:
        raise NotImplementedError
