#!/usr/bin/env python

import dxfgrabber
import random
from collections import OrderedDict

from Model.modelelement import ModelElement
from Model.parser import Parser


class DXFParser(Parser):
    def __init__(self):
        super().__init__()

    def load_file(self, file_path: str, model: ModelElement) -> None:
        dxf = dxfgrabber.readfile(file_path)
        vertices_dict = OrderedDict()

        # Detect vertices and faces
        index = 0
        faces = []
        for entity in dxf.entities:
            face_pointers = []
            # Vertices
            for vertex in entity.points:
                if vertex not in vertices_dict:
                    vertices_dict[vertex] = index
                    index += 1

                # Faces
                face_pointers.append(vertices_dict[vertex])
            faces.append(tuple(face_pointers))

        # Model data
        model.set_vertices(list(vertices_dict.keys()))
        model.set_indices(DXFParser.parse_faces(faces))
        model.set_values([random.random() for _ in range(3)])

    @staticmethod
    def parse_faces(faces: list) -> list:
        # Converts a list of 4-tuples into a list of 3-tuples
        # WARNING Why does this happen?
        # tuple((f[0], f[1], f[2])) is useful
        # tuple((f[2], f[3], f[0])) isn't useful

        return list(map(lambda x: x[:3], faces))
