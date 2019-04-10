#!/usr/bin/env python

from Model.Mesh.dxfparser import DXFParser
from Model.Mesh.offparser import OFFParser
from Model.handler import Handler


# Generic handler for mesh loading/saving
class MeshHandler(Handler):
    def __init__(self):
        super().__init__()
        self.add_parser('dxf', DXFParser())
        self.add_parser('off', OFFParser())

    def load(self, model, file_path):
        ext = Handler.get_file_extension(file_path)

        parser = self.get_parser(ext)
        parser.load_file(file_path)

        model.mesh_vertices = parser.get_vertices()
        model.mesh_indices = parser.get_indices()
        model.mesh_values = parser.get_values()

        return True

    def save(self, model, file_path: str):
        return False
