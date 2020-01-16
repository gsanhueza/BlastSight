#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pandas as pd
from qtpy.QtCore import QFileInfo
from .parserdata import ParserData
from .parser import Parser


class CSVParser(Parser):
    @staticmethod
    def load_file(path: str, *args, **kwargs) -> ParserData:
        assert path.lower().endswith('csv')

        # Metadata
        properties = {
            'name': QFileInfo(path).completeBaseName(),
            'extension': QFileInfo(path).suffix()
        }

        with open(path, 'r') as f:
            data = ParserData()
            data.data = pd.read_csv(f)
            data.properties = properties

            return data

    @staticmethod
    def save_file(*args, **kwargs) -> None:
        path = kwargs.get('path')

        if path is None:
            raise KeyError('Path missing.')

        data = pd.DataFrame(kwargs.get('data', {}))
        data.to_csv(path, index=False)
