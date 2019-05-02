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
        model.set_vertices(
            Parser.flatten_tuple(
                tuple(vertices_dict.keys())
            )
        )

        model.set_indices(
            Parser.flatten_tuple(
                self._parse_faces(faces)
            )
        )

        model.set_values(
            Parser.flatten_tuple(
                [random.random() for _ in range(3 * vertices_dict.keys().__len__())]
            )
        )

    # Converts a list of 4-tuples into a list of 3-tuples
    def _parse_faces(self, faces: list) -> list:
        ans = []
        for f in faces:
            # We need to convert 4-tuples in 3-tuples
            if len(f) == 3:
                ans.append(f)
            elif len(f) == 4:
                ans.append((f[0], f[1], f[2]))
                # WARNING Why does this work when commented?
                # ans.append((f[2], f[3], f[0]))

        return ans
