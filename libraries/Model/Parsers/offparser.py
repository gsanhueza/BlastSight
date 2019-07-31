#!/usr/bin/env python

from .parserdata import ParserData


class OFFParser:
    @staticmethod
    def load_file(file_path: str) -> ParserData:
        assert file_path.lower().endswith('off')

        with open(file_path, 'r') as fp:
            assert 'OFF' == fp.readline().strip()

            n_vertices, n_faces, n_edges = tuple([int(s) for s in fp.readline().strip().split(' ')])

            data = ParserData()
            data.vertices = [[float(s) for s in fp.readline().strip().split(' ')] for _ in range(n_vertices)]
            data.indices = [[int(s) for s in fp.readline().strip().split(' ')][1:] for _ in range(n_faces)]

            return data
