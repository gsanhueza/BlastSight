#!/usr/bin/env python

import random
from Model.parser import Parser


class OFFParser(Parser):
    def __init__(self):
        super().__init__()

    def load_file(self, file_path: str) -> None:
        import time
        start_time = time.time()

        with open(file_path, 'r') as fp:
            assert 'OFF' == fp.readline().strip()

            n_vertices, n_faces, n_edges = tuple([int(s) for s in fp.readline().strip().split(' ')])
            vertices = [[float(s) for s in fp.readline().strip().split(' ')] for i_vert in range(n_vertices)]
            faces = [[int(s) for s in fp.readline().strip().split(' ')][1:] for i_face in range(n_faces)]

            self.vertices = vertices
            self.indices = faces
            self.values = [(random.random(),
                            random.random(),
                            random.random()) for _ in range(self.vertices.__len__())]

        print(f'OFFParser    : {time.time() - start_time}')


if __name__ == '__main__':
    parser = OFFParser()
    parser.load_file('caseron.off')
    print(parser.get_vertices())
    print(parser.get_indices())
