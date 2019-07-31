#!/usr/bin/env python

import dxfgrabber
from collections import OrderedDict
from .parserdata import ParserData


class DXFParser:
    @staticmethod
    def load_file(file_path: str) -> ParserData:
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
            faces.append(face_pointers[:3])

        # Model data
        data = ParserData()
        data.vertices = list(vertices_dict.keys())
        data.indices = faces

        return data
