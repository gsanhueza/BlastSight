#!/usr/bin/env python

import dxfgrabber
from collections import OrderedDict


class DXFParser:
    def __init__(self, filepath):
        self.dxf = dxfgrabber.readfile(filepath)
        self.vertices = ()
        self.faces = ()

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
        self.faces = faces

    # Create OFF file
    # WARNING At the moment we're creating a 4-vertices OFF file
    def print_off(self):
        self._parse_entities()

        print('OFF')
        V = len(self.vertices)
        F = len(self.faces)
        E = V + F - 2
        print(f'{V} {F} {E}')
        for v in self.vertices:
            print(f'{v[0] - 73736.554} {v[1] - 57510.047} {v[2] - 362.913}')

        for f in self.faces:
            print(f'4 {f[0]} {f[1]} {f[2]} {f[3]}')


if __name__ == '__main__':
    parser = DXFParser('caseron.dxf')
    parser.print_off()
