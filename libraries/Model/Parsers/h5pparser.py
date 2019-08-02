#!/usr/bin/env python

import pandas as pd
from qtpy.QtCore import QFileInfo
from .parserdata import ParserData


class H5PParser:
    @staticmethod
    def load_file(path: str) -> ParserData:
        assert path.lower().endswith('.h5p')

        # Metadata
        properties = {
            'name': QFileInfo(path).baseName(),
            'ext': QFileInfo(path).suffix()
        }

        data = ParserData()
        data.data = pd.read_hdf(path, 'data')
        data.properties = properties

        return data

    @staticmethod
    def save_file(path: str, data) -> None:
        path = path if path.endswith('.h5p') else f'{path}.h5p'
        data.to_hdf(path, 'data')
