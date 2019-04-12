#!/usr/bin/env python

from Model.BlockModel.csvparser import CSVParser
from Model.handler import Handler


# Generic handler for block model loading/saving
class BlockModelHandler(Handler):
    def __init__(self):
        super().__init__()
        self.add_parser('csv', CSVParser())

    def load(self, model_element, file_path):
        ext = Handler.get_file_extension(file_path)

        parser = self.get_parser(ext)
        parser.load_file(file_path)

        model_element.set_vertices(parser.get_vertices())
        model_element.set_indices(parser.get_indices())
        model_element.set_values(parser.get_values())

        return True

    def save(self, model, file_path: str):
        return False
