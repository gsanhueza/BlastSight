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

    def get_averaged_vertices(self):
        avg_tuple = self._avg_tuple(list(self.vertices))
        return self.flatten_tuple((x[0] - avg_tuple[0],
                                   x[1] - avg_tuple[1],
                                   x[2] - avg_tuple[2]) for x in list(self.vertices))

    # Averages each component of a list of n-tuples in a new n-tuple
    def _avg_tuple(self, tuple_list: list):
        if len(tuple_list) == 0:
            return None

        len_tuple = len(tuple_list[0])
        accum = [0] * len_tuple

        for _tuple in tuple_list:
            for i in range(len_tuple):
                accum[i] += _tuple[i]

        return tuple(map(lambda x: x / len(tuple_list), accum))


if __name__ == '__main__':
    parser = DXFParser()
    parser.load_file('caseron.dxf')
    print(parser.get_vertices())
    print(parser.vertices)
    print(parser.get_averaged_vertices())
