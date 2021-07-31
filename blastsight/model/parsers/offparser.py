#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
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

        # Process header
        with open(path, 'r') as fp:
            assert 'OFF' == fp.readline().strip()
            n_vertices, n_faces, n_edges = map(int, fp.readline().strip().split(' '))

        # Process vertices
        vertices = pd.read_csv(path, skiprows=1, nrows=n_vertices, usecols=range(3), sep=' ').to_numpy(dtype=float)

        # Pre-process indices "columns" (Simplify loading OFF files with variable column numbers in indices)
        with open(path, 'r') as temp_f:
            col_count = [len(line.split(' ')) for line in temp_f.readlines()]

        # Process indices
        indices = []
        raw_indices = pd.read_csv(path, skiprows=n_vertices + 2, nrows=n_faces, delimiter=' ',
                                  header=None, names=list(map(str, range(max(col_count)))))

        # Accept indices directly if they all describe only triangles
        if raw_indices.iloc[:, 0].max() == 3:
            indices = raw_indices[raw_indices.columns[-3:]].to_numpy(dtype=int)

        # Triangulate polygons otherwise
        else:
            for _, idx in raw_indices.iterrows():
                counter = idx[0]
                row_indices = idx.to_numpy(dtype=int)[1:]
                fan_starter = row_indices[0]
                fan_indices = row_indices[1:]

                while counter > 2:
                    indices += [fan_starter, fan_indices[0], fan_indices[1]]
                    fan_indices = fan_indices[1:]
                    counter -= 1

            indices = np.array(indices, np.int32).reshape((-1, 3))

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
