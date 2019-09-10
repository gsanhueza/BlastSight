#!/usr/bin/env python

import pandas as pd

from qtpy.QtCore import QFileInfo
from .parserdata import ParserData
from .parser import Parser


class OFFParser(Parser):
    @staticmethod
    def load_file(path: str) -> ParserData:
        assert path.lower().endswith('off')

        with open(path, 'r') as fp:
            assert 'OFF' == fp.readline().strip()
            n_vertices, n_faces, n_edges = tuple([int(s) for s in fp.readline().strip().split(' ')])

            vertices = pd.read_csv(path, skiprows=1, nrows=n_vertices,
                                   usecols=range(3), sep=' ').to_numpy(dtype=float)
            indices = pd.read_csv(path, skiprows=1 + n_vertices, nrows=n_faces, delimiter=' ',
                                  usecols=range(1, 4)).to_numpy(dtype=int)

            # Metadata
            properties = {
                'name': QFileInfo(path).completeBaseName(),
                'ext': QFileInfo(path).suffix()
            }

            data = ParserData()
            data.vertices = vertices
            data.indices = indices
            data.properties = properties

            return data
