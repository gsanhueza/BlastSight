#!/usr/bin/env python

from Model.modelelement import ModelElement


class Parser:
    def __init__(self):
        pass

    def load_file(self, file_path: str, model: ModelElement) -> None:
        pass

    # Flatten list of tuples
    @staticmethod
    def flatten_tuple(l: list) -> list:
        try:
            return [item for sublist in l for item in sublist]
        except TypeError:
            return l
