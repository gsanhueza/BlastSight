#!/usr/bin/env python

import dxfgrabber
from qtpy.QtCore import QFileInfo
from collections import OrderedDict
from .parserdata import ParserData


class DXFParser:
    @staticmethod
    def load_file(path: str) -> ParserData:
        assert path.lower().endswith('dxf')

        dxf = dxfgrabber.readfile(path)
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

        # Metadata
        properties = {
            'name': QFileInfo(path).completeBaseName(),
            'ext': QFileInfo(path).suffix()
        }

        # Model data
        data = ParserData()
        data.vertices = list(vertices_dict.keys())
        data.indices = faces
        data.properties = properties

        return data
