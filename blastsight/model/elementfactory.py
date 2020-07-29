#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .elements.nullelement import NullElement
from .elements.meshelement import MeshElement
from .elements.blockelement import BlockElement
from .elements.pointelement import PointElement
from .elements.lineelement import LineElement
from .elements.tubeelement import TubeElement


class ElementFactory:
    @staticmethod
    def null(*args, **kwargs) -> NullElement:
        return NullElement(*args, **kwargs)

    @staticmethod
    def mesh(*args, **kwargs) -> MeshElement:
        return MeshElement(*args, **kwargs)

    @staticmethod
    def blocks(*args, **kwargs) -> BlockElement:
        return BlockElement(*args, **kwargs)

    @staticmethod
    def points(*args, **kwargs) -> PointElement:
        return PointElement(*args, **kwargs)

    @staticmethod
    def lines(*args, **kwargs) -> LineElement:
        return LineElement(*args, **kwargs)

    @staticmethod
    def tubes(*args, **kwargs) -> TubeElement:
        return TubeElement(*args, **kwargs)
