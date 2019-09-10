#!/usr/bin/env python

import multiprocessing
import pandas as pd

from qtpy.QtCore import QFileInfo
from .parserdata import ParserData
from .parser import Parser


class OFFParser(Parser):
    """
    Pandas' current version (0.25) has an ugly memory leak when reading files (tested empirically).
    Since MineVis is not meant to improve Pandas, we'll implement a workaround from
    https://stackoverflow.com/a/39101287 (multiprocessing) with some bits from
    https://stackoverflow.com/a/46322731 (pool.join(), pool.close())

    """
    @staticmethod
    def _load_file_mp(path: str) -> ParserData:
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

    @staticmethod
    def load_file(path: str) -> ParserData:
        pool = multiprocessing.Pool(1)
        result = pool.map(OFFParser._load_file_mp, [path])[0]
        pool.close()
        pool.join()
        del pool

        return result
