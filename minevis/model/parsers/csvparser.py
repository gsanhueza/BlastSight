#!/usr/bin/env python

import multiprocessing
import pandas as pd
from qtpy.QtCore import QFileInfo
from .parserdata import ParserData
from .parser import Parser


class CSVParser(Parser):
    """
    Pandas' current version (0.25) has an ugly memory leak when reading files (tested empirically).
    Since MineVis is not meant to improve Pandas, we'll implement a workaround from
    https://stackoverflow.com/a/39101287 (multiprocessing) with some bits from
    https://stackoverflow.com/a/46322731 (pool.join(), pool.close())

    """
    @staticmethod
    def _load_file_mp(path: str) -> ParserData:
        assert path.lower().endswith('csv')

        # Metadata
        properties = {
            'name': QFileInfo(path).completeBaseName(),
            'ext': QFileInfo(path).suffix()
        }

        with open(path, 'r') as f:
            data = ParserData()
            data.data = pd.read_csv(f)
            data.properties = properties

            return data

    @staticmethod
    def load_file(path: str) -> ParserData:
        pool = multiprocessing.Pool(1)
        result = pool.map(CSVParser._load_file_mp, [path])[0]
        pool.close()
        pool.join()
        del pool

        return result

    @staticmethod
    def save_file(*args, **kwargs) -> None:
        path = kwargs.get('path', None)

        if path is None:
            raise KeyError('Path missing.')

        data = kwargs.get('data', pd.DataFrame())
        data.to_csv(path, index=False)
