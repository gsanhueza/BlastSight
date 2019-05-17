#!/usr/bin/env python


class OFFParser:
    @staticmethod
    def load_file(file_path: str) -> tuple:
        assert file_path.lower().endswith('off')

        with open(file_path, 'r') as fp:
            assert 'OFF' == fp.readline().strip()

            n_vertices, n_faces, n_edges = tuple([int(s) for s in fp.readline().strip().split(' ')])

            return [[float(s) for s in fp.readline().strip().split(' ')] for _ in range(n_vertices)],\
                   [[int(s) for s in fp.readline().strip().split(' ')][1:] for _ in range(n_faces)]
