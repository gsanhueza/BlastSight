#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import dxfgrabber
import numpy as np

from qtpy.QtCore import QFileInfo
from .parserdata import ParserData
from .parser import Parser


class DXFParser(Parser):
    @staticmethod
    def load_file(path: str, *args, **kwargs) -> ParserData:
        assert path.lower().endswith('dxf')

        dxf = dxfgrabber.readfile(path)

        # Model data
        data = ParserData()
        points = []

        def fill_as_mesh():
            entities = [e for e in dxf.entities if type(e) in [dxfgrabber.dxfentities.Face]]

            for entity in entities:
                points.extend(entity.points[:3])

            # Detect vertices and indices
            vertices, indices = np.unique(np.array(points), axis=0, return_inverse=True)
            data.vertices = vertices
            data.indices = indices.reshape((-1, 3))

        def fill_as_polyline():
            # Detect vertices and indices
            entities = [e for e in dxf.entities if type(e) in [dxfgrabber.dxfentities.Polyline,
                                                               dxfgrabber.dxfentities.LWPolyline]]

            for entity in entities:
                points.extend(entity.points)
            # Detect vertices only
            data.vertices = np.array(points)

        # Fill depending on the given hint
        if kwargs.get('hint', 'mesh') == 'mesh':
            fill_as_mesh()
        else:
            fill_as_polyline()

        # Metadata
        data.properties = {
            'name': QFileInfo(path).completeBaseName(),
            'extension': QFileInfo(path).suffix()
        }

        return data

    @staticmethod
    def save_file(path: str, *args, **kwargs) -> None:
        raise NotImplementedError
