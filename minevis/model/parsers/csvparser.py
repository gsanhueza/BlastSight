#!/usr/bin/env python

import pandas as pd
from qtpy.QtCore import QFileInfo
from .parserdata import ParserData
from .parser import Parser


class CSVParser(Parser):
    @staticmethod
    def load_file(path: str) -> ParserData:
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
    def save_file(path: str, *args, **kwargs):
        raise NotImplementedError
