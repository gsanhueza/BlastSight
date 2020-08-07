#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pandas as pd
from qtpy.QtCore import QFileInfo
from .parser import Parser


class CSVParser(Parser):
    @staticmethod
    def load_file(path: str, *args, **kwargs) -> dict:
        assert path.lower().endswith('csv')

        # Data
        with open(path, 'r') as f:
            data = pd.read_csv(f)

        # Properties
        properties = {}

        # Metadata
        metadata = {
            'name': QFileInfo(path).completeBaseName(),
            'extension': QFileInfo(path).suffix()
        }

        return {
            'data': data,
            'properties': properties,
            'metadata': metadata,
        }

    @staticmethod
    def save_file(*args, **kwargs) -> None:
        path = kwargs.get('path')

        if path is None:
            raise IOError('Path missing.')

        data = pd.DataFrame(kwargs.get('data', {}))
        data.to_csv(path, index=False)
