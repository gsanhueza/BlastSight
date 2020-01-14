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

        hints = {'mesh': [dxfgrabber.dxfentities.Face],
                 'line': [dxfgrabber.dxfentities.Polyline, dxfgrabber.dxfentities.LWPolyline],
                 'tube': [dxfgrabber.dxfentities.Polyline, dxfgrabber.dxfentities.LWPolyline],
                 }

        # Detect vertices and indices
        entities = [e for e in dxf.entities if type(e) in hints.get(kwargs.get('hint', 'mesh'))]
        points = []

        for entity in entities:
            points.extend(entity.points[:3])
        vertices, indices = np.unique(np.array(points), axis=0, return_inverse=True)

        # Metadata
        properties = {
            'name': QFileInfo(path).completeBaseName(),
            'extension': QFileInfo(path).suffix()
        }

        # Model data
        data = ParserData()
        data.vertices = vertices
        data.indices = indices.reshape((-1, 3))
        data.properties = properties

        return data
