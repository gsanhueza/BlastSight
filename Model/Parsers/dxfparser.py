#!/usr/bin/env python

import dxfgrabber
from collections import OrderedDict


class DXFParser:
    @staticmethod
    def load_file(file_path: str) -> tuple:
        assert file_path.lower().endswith('dxf')

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
        return list(vertices_dict.keys()), DXFParser.parse_faces(faces)

    @staticmethod
    def parse_faces(faces: list) -> list:
        # Converts a list of 4-tuples into a list of 3-tuples
        # WARNING Why does this happen?
        # tuple((f[0], f[1], f[2])) is useful
        # tuple((f[2], f[3], f[0])) isn't useful

        return list(map(lambda x: x[:3], faces))
