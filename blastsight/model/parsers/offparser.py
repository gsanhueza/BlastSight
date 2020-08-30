#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
import pandas as pd

from qtpy.QtCore import QFileInfo
from .parser import Parser


class OFFParser(Parser):
    @staticmethod
    def load_file(path: str, *args, **kwargs) -> dict:
        assert path.lower().endswith('off')

        with open(path, 'r') as fp:
            assert 'OFF' == fp.readline().strip()
            n_vertices, n_faces, n_edges = map(int, fp.readline().strip().split(' '))

            vertices = pd.read_csv(path, skiprows=1, nrows=n_vertices,
                                   usecols=range(3), sep=' ').to_numpy(dtype=float)
            indices = pd.read_csv(path, skiprows=1 + n_vertices, nrows=n_faces, delimiter=' ',
                                  usecols=range(1, 4)).to_numpy(dtype=int)

        # Data
        data = {
            'vertices': vertices,
            'indices': indices,
        }

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
    def save_file(path: str, *args, **kwargs) -> None:
        if path is None:
            raise KeyError('Path missing.')

        vertices = kwargs.get('vertices')
        indices = kwargs.get('indices')

        if vertices is None:
            data = kwargs.get('data', {})
            if 'vertices' in data.keys():
                vertices = data['vertices']
            else:
                vertices = np.column_stack((data.get('x', []),
                                            data.get('y', []),
                                            data.get('z', []),
                                            ))

            indices = indices or data.get('indices', [])

        V = len(vertices)
        F = len(indices)
        E = V + F - 2

        # Internal data
        with open(path, 'w') as f:
            f.write('OFF\n')
            f.write(f'{V} {F} {E}\n')

        # Vertices
        pd.DataFrame(vertices).to_csv(path, mode='a', sep=' ', header=False, index=False)

        # Indices
        pd.DataFrame(np.column_stack(([[3]] * len(indices), indices))).to_csv(
            path, mode='a', sep=' ', header=False, index=False)
