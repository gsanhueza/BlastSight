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
        return NullElement(hint='null', *args, **kwargs)

    @staticmethod
    def mesh(*args, **kwargs) -> MeshElement:
        return MeshElement(hint='mesh', *args, **kwargs)

    @staticmethod
    def blocks(*args, **kwargs) -> BlockElement:
        return BlockElement(hint='block', *args, **kwargs)

    @staticmethod
    def points(*args, **kwargs) -> PointElement:
        return PointElement(hint='point', *args, **kwargs)

    @staticmethod
    def lines(*args, **kwargs) -> LineElement:
        return LineElement(hint='line', *args, **kwargs)

    @staticmethod
    def tubes(*args, **kwargs) -> TubeElement:
        return TubeElement(hint='tube', *args, **kwargs)
