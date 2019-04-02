#!/usr/bin/env python

import dxfgrabber
from collections import OrderedDict


class DXFParser:
    def __init__(self, filepath=None):
        # FIXME Do you really want to work with tuples?
        self.vertices = tuple()
        self.faces = tuple()
        self.dxf = None

        if filepath:
            self.load(filepath)

    def load_dxffile(self, filepath: str) -> None:
        self.dxf = dxfgrabber.readfile(filepath)
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
        self.faces = self._parse_faces(faces)

    # Converts a list of 4-tuples into a list of 3-tuples
    def _parse_faces(self, faces: list) -> list:
        ans = []
        for f in faces:
            # We need to convert 4-tuples in 3-tuples
            if len(f) == 3:
                ans.append(f)
            elif len(f) == 4:
                ans.append((f[0], f[1], f[2]))
                #ans.append((f[2], f[3], f[0]))  # WARNING Is there a reason for this to work better if commented?

        return ans

    def get_vertices(self):
        return [item for sublist in self.vertices for item in sublist]  # Flatten list of tuples

    def get_faces(self):
        return self.faces

    # Returns the average of each component of a list of n-tuples in a new n-tuple
    def _avg_tuple(self, tuple_list: list):
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
        V = len(self.get_vertices())
        F = len(self.get_faces())
        E = V + F - 2

        string_builder = ['OFF', f'{V} {F} {E}']

        for v in self.get_vertices():
            avg_tuple = self._avg_tuple(self.get_vertices())  # WARNING This is only used to center the triangulation
            string_builder.append(' '.join(map(str, tuple(map(lambda x, y: x - y, v, avg_tuple)))))

        for f in self.get_faces():
            string_builder.append(' '.join(map(str, tuple((3,) + f))))

        return '\n'.join(string_builder)

    def print_off(self):
        print(self._build_string())


if __name__ == '__main__':
    parser = DXFParser()
    parser.load_dxffile('caseron.dxf')
    parser.print_off()
