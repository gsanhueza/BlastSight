#!/usr/bin/env python

import pandas as pd
from qtpy.QtCore import QFileInfo
from .parserdata import ParserData


class H5PParser:
    @staticmethod
    def load_file(path: str) -> ParserData:
        assert path.lower().endswith('.h5p')

        store = pd.HDFStore(path)
        properties = store.get_storer('data').attrs.metadata

        # Metadata
        properties['name'] = QFileInfo(path).baseName()
        properties['ext'] = QFileInfo(path).suffix()

        data = ParserData()
        data.data = store['data']
        data.properties = properties

        return data

    @staticmethod
    def save_file(path: str, data, properties={}) -> None:
        path = path if path.endswith('.h5p') else f'{path}.h5p'

        store = pd.HDFStore(path)
        store.put('data', data)
        store.get_storer('data').attrs.metadata = properties
        store.close()
