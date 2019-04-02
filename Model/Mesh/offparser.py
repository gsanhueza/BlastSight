#!/usr/bin/env python

from .parser import Parser


class OFFParser(Parser):
    def __init__(self, filepath=None):
        self.vertices = None
        self.faces = None
        self.filepath = filepath

    def load_file(self, filepath: str) -> None:
        pass
