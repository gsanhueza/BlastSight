#!/usr/bin/env python

import random
from Model.parser import Parser


class OFFParser(Parser):
    def __init__(self):
        super().__init__()

    def load_file(self, file_path: str) -> None:
        with open(file_path, 'r') as fp:
            lines = fp.readlines()
            lines = [line.strip() for line in lines]

            assert lines[0] == 'OFF'

            parts = lines[1].split(' ')
            assert len(parts) == 3

            num_vertices = int(parts[0])
            assert num_vertices > 0

            num_faces = int(parts[1])
            assert num_faces > 0

            vertices = []
            for i in range(num_vertices):
                vertex = lines[2 + i].split(' ')
                vertex = [float(point) for point in vertex]
                assert len(vertex) == 3

                vertices.append(vertex)

            faces = []
            for i in range(num_faces):
                face = lines[2 + num_vertices + i].split(' ')
                face = [int(index) for index in face]

                assert face[0] == len(face) - 1
                for index in face:
                    assert 0 <= index < num_vertices

                assert len(face) > 1

                faces.append(face[1:])

            self.vertices = vertices
            self.indices = faces
            self.values = [(random.random(),
                            random.random(),
                            random.random()) for _ in range(self.vertices.__len__())]


if __name__ == '__main__':
    parser = OFFParser()
    parser.load_file('caseron.off')
    print(parser.get_vertices())
    print(parser.get_indices())
