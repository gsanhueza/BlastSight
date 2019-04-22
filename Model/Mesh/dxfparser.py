#!/usr/bin/env python

import dxfgrabber
import random
from collections import OrderedDict

from Model.parser import Parser


class DXFParser(Parser):
    def __init__(self):
        super().__init__()
        self.dxf = None

    def load_file(self, file_path: str) -> None:
        self.dxf = dxfgrabber.readfile(file_path)
        self._parse_entities()

    # Returns the entities of the DXF file
    def get_entities(self):
        return self.dxf.entities

    # Read the DXF file and create tuples of vertices and faces
    def _parse_entities(self) -> None:
        vertices_dict = OrderedDict()
        # Detect vertices and faces
        index = 0
        faces = []
        for entity in self.get_entities():
            face_pointers = []
            # Vertices
            for vertex in entity.points:
                if vertex not in vertices_dict:
                    vertices_dict[vertex] = index
                    index += 1

                # Faces
                face_pointers.append(vertices_dict[vertex])
            faces.append(tuple(face_pointers))

        self.vertices = tuple(vertices_dict.keys())
        self.indices = self._parse_faces(faces)
        self.values = [(random.random(),
                        random.random(),
                        random.random()) for _ in range(self.vertices.__len__())]

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


if __name__ == '__main__':
    parser = DXFParser()
    parser.load_file('caseron.dxf')
    print(parser.get_vertices())
    print(parser.vertices)
