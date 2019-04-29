#!/usr/bin/env python

from Model.modelelement import ModelElement
from Model.Mesh.dxfparser import DXFParser
from Model.Mesh.offparser import OFFParser


# Main class
class MeshElement(ModelElement):
    def __init__(self):
        super().__init__()
        self.add_parser('dxf', DXFParser())
        self.add_parser('off', OFFParser())
