#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
import pandas as pd

from qtpy.QtCore import QFileInfo
from .parserdata import ParserData
from .parser import Parser


class OFFParser(Parser):
    @staticmethod
    def load_file(path: str, *args, **kwargs) -> ParserData:
        assert path.lower().endswith('off')

        with open(path, 'r') as fp:
            assert 'OFF' == fp.readline().strip()
            n_vertices, n_faces, n_edges = tuple([int(s) for s in fp.readline().strip().split(' ')])

            vertices = pd.read_csv(path, skiprows=1, nrows=n_vertices,
                                   usecols=range(3), sep=' ').to_numpy(dtype=float)
            indices = pd.read_csv(path, skiprows=1 + n_vertices, nrows=n_faces, delimiter=' ',
                                  usecols=range(1, 4)).to_numpy(dtype=int)

            # Metadata
            properties = {
                'name': QFileInfo(path).completeBaseName(),
                'extension': QFileInfo(path).suffix()
            }

            data = ParserData()
            data.vertices = vertices
            data.indices = indices
            data.properties = properties

            return data

    @staticmethod
    def save_file(path: str, *args, **kwargs) -> None:
        if path is None:
            raise KeyError('Path missing.')

        vertices = kwargs.get('vertices', None)
        indices = kwargs.get('indices', None)

        if vertices is None:
            data = kwargs.get('data', {})
            try:
                vertices = data['vertices']
            except Exception as e:
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
