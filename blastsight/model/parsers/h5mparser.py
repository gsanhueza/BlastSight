#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import h5py
import numpy as np
from qtpy.QtCore import QFileInfo
from .parser import Parser


class H5MParser(Parser):
    @staticmethod
    def load_file(path: str, *args, **kwargs) -> dict:
        with h5py.File(path, 'r') as hf:
            vertices = hf['vertices'][()]
            indices = hf['indices'][()]

            # Properties
            properties = dict(hf.attrs)

        # Data
        data = {
            'vertices': vertices,
            'indices': indices,
        }

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

        vertices = kwargs.get('vertices')
        indices = kwargs.get('indices')

        if vertices is None:
            data = kwargs.get('data', {})
            try:
                vertices = data['vertices']
            except Exception:
                vertices = np.column_stack((data.get('x', []),
                                            data.get('y', []),
                                            data.get('z', []),
                                            ))

            indices = indices or data.get('indices', [])

        properties = kwargs.get('properties', {})

        with h5py.File(path, 'w') as hf:
            hf.create_dataset('vertices', data=vertices, dtype='float32')
            hf.create_dataset('indices', data=indices, dtype='uint32')

            for k, v in properties.items():
                hf.attrs[k] = v
