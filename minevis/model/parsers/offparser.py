#!/usr/bin/env python

from qtpy.QtCore import QFileInfo
from .parserdata import ParserData


class OFFParser:
    @staticmethod
    def load_file(path: str) -> ParserData:
        assert path.lower().endswith('off')

        with open(path, 'r') as fp:
            assert 'OFF' == fp.readline().strip()

            n_vertices, n_faces, n_edges = tuple([int(s) for s in fp.readline().strip().split(' ')])

            # Metadata
            properties = {
                'name': QFileInfo(path).completeBaseName(),
                'ext': QFileInfo(path).suffix()
            }

            data = ParserData()
            data.vertices = [[float(s) for s in fp.readline().strip().split(' ')] for _ in range(n_vertices)]
            data.indices = [[int(s) for s in fp.readline().strip().split(' ')][1:] for _ in range(n_faces)]
            data.properties = properties

            return data
