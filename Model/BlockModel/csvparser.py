#!/usr/bin/env python

from Model.parser import Parser


class CSVParser(Parser):
    def __init__(self):
        super().__init__()

    def load_file(self, filepath: str) -> None:
        pass
