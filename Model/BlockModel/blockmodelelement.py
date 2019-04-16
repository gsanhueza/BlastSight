#!/usr/bin/env python

from Model.modelelement import ModelElement
from Model.BlockModel.csvparser import CSVParser


# Main class
class BlockModelElement(ModelElement):
    def __init__(self):
        super().__init__()
        self.add_parser('csv', CSVParser())
