#!/usr/bin/env python

import h5py
from qtpy.QtCore import QFileInfo
from .parserdata import ParserData


class H5MParser:
    @staticmethod
    def load_file(path: str) -> ParserData:
        assert path.lower().endswith('.h5m')

        hf = h5py.File(path, 'r')
        vertices = hf['vertices'][()]
        indices = hf['indices'][()]
        properties = dict(hf.attrs)
        hf.close()

        # Metadata
        properties['name'] = QFileInfo(path).completeBaseName()
        properties['ext'] = QFileInfo(path).suffix()

        data = ParserData()
        data.vertices = vertices
        data.indices = indices
        data.properties = properties

        return data

    @staticmethod
    def save_file(path: str, vertices, indices, properties={}) -> None:
        path = path if path.endswith('.h5m') else f'{path}.h5m'
        hf = h5py.File(path, 'w')
        hf.create_dataset('vertices', data=vertices, dtype='float32')
        hf.create_dataset('indices', data=indices, dtype='uint32')

        for k, v in properties.items():
            hf.attrs[k] = v

        hf.close()
