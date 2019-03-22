#!/usr/bin/env python

# TODO Importar algun parser de DXF
# TODO Leer solo los "entities"
# TODO Transformar lo leido a un archivo OFF (por ejemplo)

import dxfgrabber
from collections import OrderedDict


class DXFParser:
    def __init__(self, filepath):
        self.dxf = dxfgrabber.readfile(filepath)

    def get_entities(self):
        return self.dxf.entities


if __name__ == '__main__':
    parser = DXFParser('caseron.dxf')

    vertices_dict = OrderedDict()
    # Detect vertices
    index = 0
    for entity in parser.get_entities():
        for vertex in entity.points:
            if vertex not in vertices_dict:
                vertices_dict[vertex] = index
                index += 1

    # Detect faces
    faces = []
    for entity in parser.get_entities():
        face_pointers = []
        for vertex in entity.points:
            face_pointers.append(vertices_dict[vertex])
        faces.append(tuple(face_pointers))

    # Create OFF file
    print('OFF')
    V = len(vertices_dict)
    F = len(faces)
    E = V + F - 2
    print(f'{V} {F} {E}')
    for v in vertices_dict.keys():
        print(f'{v[0] - 73736.554} {v[1] - 57510.047} {v[2] - 362.913}')

    for f in faces:
        print(f'4 {f[0]} {f[1]} {f[2]} {f[3]}')
