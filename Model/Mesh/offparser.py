#!/usr/bin/env python

from .parser import Parser


class OFFParser(Parser):
    def __init__(self):
        super().__init__()

    def load_file(self, filepath: str) -> None:
        pass
