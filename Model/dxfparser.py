#!/usr/bin/env python

import dxfgrabber
from collections import OrderedDict


class DXFParser:
    def __init__(self, filepath=None):
        self.vertices = tuple()
        self.faces = tuple()
        self.dxf = None

        if filepath:
            self.load(filepath)

    def load_dxffile(self, filepath):
        self.dxf = dxfgrabber.readfile(filepath)

    # Returns the entities of the DXF file
    def get_entities(self):
        return self.dxf.entities

    # Read the DXF file and create tuples of vertices and faces
    def _parse_entities(self):
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
        self.faces = self._parse_faces(faces)

    # Converts a list of 4-tuples into a list of 3-tuples
    def _parse_faces(self, faces):
        ans = []
        for f in faces:
            # We need to convert 4-tuples in 3-tuples
            if len(f) == 3:
                ans.append(f)
            elif len(f) == 4:
                ans.append((f[0], f[1], f[2]))
                #ans.append((f[2], f[3], f[0]))  # WARNING Is there a reason for this to work better if commented?

        return ans

    # Returns the average of each component of a list of n-tuples in a new n-tuple
    def _avg_tuple(self, tuple_list):
        if len(tuple_list) == 0:
            return None

        len_tuple = len(tuple_list[0])
        accum = [0] * len_tuple

        for _tuple in tuple_list:
            for i in range(len_tuple):
                accum[i] += _tuple[i]

        return tuple(map(lambda x: x / len(tuple_list), accum))

    # Create OFF file
    def _build_string(self):
        self._parse_entities()

        V = len(self.vertices)
        F = len(self.faces)
        E = V + F - 2

        string_builder = []
        string_builder.append('OFF')
        string_builder.append(f'{V} {F} {E}')

        for v in self.vertices:
            avg_tuple = self._avg_tuple(self.vertices) # WARNING This is only used to center the triangulation
            string_builder.append(f'{v[0] - avg_tuple[0]} {v[1] - avg_tuple[1]} {v[2] - avg_tuple[2]}')

        for f in self.faces:
            string_builder.append(f'3 {f[0]} {f[1]} {f[2]}')

        return '\n'.join(string_builder)

    def print_off(self):
        print(self._build_string())


if __name__ == '__main__':
    parser = DXFParser()
    parser.load_dxffile('caseron.dxf')
    parser.print_off()
