#!/usr/bin/env python

import pandas as pd
from qtpy.QtCore import QFileInfo
from .parserdata import ParserData


class OUTParser:
    @staticmethod
    def load_file(path: str) -> ParserData:
        assert path.lower().endswith('out')

        # Metadata
        properties = {
            'name': QFileInfo(path).completeBaseName(),
            'ext': QFileInfo(path).suffix()
        }

        with open(path, 'r') as f:
            data = ParserData()
            data.data = pd.read_csv(f, header=None, prefix='col_', sep=' ')
            data.properties = properties

            return data
