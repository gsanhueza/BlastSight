#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pandas as pd
from qtpy.QtCore import QFileInfo
from .parser import Parser


class H5PParser(Parser):
    @staticmethod
    def load_file(path: str, *args, **kwargs) -> dict:
        with pd.HDFStore(path, 'r') as store:
            # Data
            data = store.get('data')

            # Properties
            try:
                properties = store.get_storer('data').attrs.metadata
            except AttributeError:
                properties = {}

        # Metadata
        metadata = {
            'name': QFileInfo(path).completeBaseName(),
            'extension': QFileInfo(path).suffix(),
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
            raise KeyError('Path missing.')

        data = kwargs.get('data', [])
        properties = kwargs.get('properties', {})

        with pd.HDFStore(path, 'w') as store:
            store.put('data', data)
            store.get_storer('data').attrs.metadata = properties
