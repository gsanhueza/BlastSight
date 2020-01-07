#!/usr/bin/env python


#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

class ParserData:
    def __init__(self):
        """
        For meshes:
        {
            'data': {
                'vertices': list[list[float]],
                'indices': list[int]
            },
            'properties': {
                'color': list[float],
                'alpha': float
            }
        }

        For blocks/points:
        {
            'data': Pandas DataFrame,
            'properties': dict of properties
        }
        """
        self._data = {'data': {}, 'properties': {}}

    @property
    def vertices(self) -> list:
        return self._data.get('data', {}).get('vertices', [])

    @property
    def indices(self) -> list:
        return self._data.get('data', {}).get('indices', [])

    @property
    def data(self) -> dict:
        return self._data.get('data', {})

    @property
    def properties(self) -> dict:
        return self._data.get('properties', {})

    @vertices.setter
    def vertices(self, _data) -> None:
        self._data['data']['vertices'] = _data

    @indices.setter
    def indices(self, _data) -> None:
        self._data['data']['indices'] = _data

    @data.setter
    def data(self, _data) -> None:
        self._data['data'] = _data

    @properties.setter
    def properties(self, _data) -> None:
        self._data['properties'] = _data
