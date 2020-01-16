#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import h5py
import numpy as np
from qtpy.QtCore import QFileInfo
from .parserdata import ParserData
from .parser import Parser


class H5MParser(Parser):
    @staticmethod
    def load_file(path: str, *args, **kwargs) -> ParserData:
        hf = h5py.File(path, 'r')
        vertices = hf['vertices'][()]
        indices = hf['indices'][()]
        properties = dict(hf.attrs)
        hf.close()

        # Metadata
        properties['name'] = QFileInfo(path).completeBaseName()
        properties['extension'] = QFileInfo(path).suffix()

        data = ParserData()
        data.vertices = vertices
        data.indices = indices
        data.properties = properties

        return data

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

        hf = h5py.File(path, 'w')
        hf.create_dataset('vertices', data=vertices, dtype='float32')
        hf.create_dataset('indices', data=indices, dtype='uint32')

        for k, v in properties.items():
            hf.attrs[k] = v

        hf.close()
