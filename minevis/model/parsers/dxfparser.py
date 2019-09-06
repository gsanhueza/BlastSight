#!/usr/bin/env python

import dxfgrabber
import numpy as np

from qtpy.QtCore import QFileInfo
from .parserdata import ParserData
from .parser import Parser


class DXFParser(Parser):
    @staticmethod
    def load_file(path: str) -> ParserData:
        assert path.lower().endswith('dxf')

        dxf = dxfgrabber.readfile(path)

        # Detect vertices and indices
        points = []
        for entity in dxf.entities:
            points += entity.points[:3]
        vertices, indices = np.unique(np.array(points), axis=0, return_inverse=True)

        # Metadata
        properties = {
            'name': QFileInfo(path).completeBaseName(),
            'ext': QFileInfo(path).suffix()
        }

        # Model data
        data = ParserData()
        data.vertices = vertices
        data.indices = indices.reshape((indices.size // 3, 3))
        data.properties = properties

        return data
