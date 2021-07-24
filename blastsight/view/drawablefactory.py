#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import traceback

from .drawables.gldrawable import GLDrawable
from .drawables.axisgl import AxisGL
from .drawables.backgroundgl import BackgroundGL

from .drawables.meshgl import MeshGL
from .drawables.blockgl import BlockGL
from .drawables.pointgl import PointGL
from .drawables.linegl import LineGL
from .drawables.tubegl import TubeGL

from .drawables.blocklegacygl import BlockLegacyGL
from .drawables.tubelegacygl import TubeLegacyGL

from .drawables.textgl import TextGL
from .drawables.gridgl import GridGL


class DrawableFactory:
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

    @staticmethod
    def generate_drawable(d_class: type, generator: callable, *args, **kwargs) -> GLDrawable or None:
        try:
            element = generator(*args, **kwargs)
            drawable = d_class(element, *args, **kwargs)

            return drawable
        except Exception:
            traceback.print_exc()
            return None

    """
    Drawables by arguments
    """
    def axis(self, *args, **kwargs) -> AxisGL:
        return self.generate_drawable(AxisGL, self.engine.null, *args, **kwargs)

    def background(self, *args, **kwargs) -> BackgroundGL:
        return self.generate_drawable(BackgroundGL, self.engine.null, *args, **kwargs)

    def mesh(self, *args, **kwargs) -> MeshGL:
        return self.generate_drawable(MeshGL, self.engine.mesh, *args, **kwargs)

    def blocks(self, *args, **kwargs) -> BlockGL:
        if kwargs.pop('legacy', False):
            return self.generate_drawable(BlockLegacyGL, self.engine.blocks, *args, **kwargs)
        return self.generate_drawable(BlockGL, self.engine.blocks, *args, **kwargs)

    def points(self, *args, **kwargs) -> PointGL:
        return self.generate_drawable(PointGL, self.engine.points, *args, **kwargs)

    def lines(self, *args, **kwargs) -> LineGL:
        return self.generate_drawable(LineGL, self.engine.lines, *args, **kwargs)

    def tubes(self, *args, **kwargs) -> TubeGL:
        if kwargs.pop('legacy', False):
            return self.generate_drawable(TubeLegacyGL, self.engine.tubes, *args, **kwargs)
        return self.generate_drawable(TubeGL, self.engine.tubes, *args, **kwargs)

    def text(self, *args, **kwargs) -> TextGL:
        return self.generate_drawable(TextGL, self.engine.text, *args, **kwargs)

    def grid(self, *args, **kwargs) -> GridGL:
        return self.generate_drawable(GridGL, self.engine.null, *args, **kwargs)

    """
    Drawables by path
    """
    def load_mesh(self, path: str, *args, **kwargs) -> MeshGL:
        return self.generate_drawable(MeshGL, self.engine.load_mesh, path, *args, **kwargs)

    def load_blocks(self, path: str, *args, **kwargs) -> BlockGL:
        return self.generate_drawable(BlockGL, self.engine.load_blocks, path, *args, **kwargs)

    def load_points(self, path: str, *args, **kwargs) -> PointGL:
        return self.generate_drawable(PointGL, self.engine.load_points, path, *args, **kwargs)

    def load_lines(self, path: str, *args, **kwargs) -> LineGL:
        return self.generate_drawable(LineGL, self.engine.load_lines, path, *args, **kwargs)

    def load_tubes(self, path: str, *args, **kwargs) -> TubeGL:
        return self.generate_drawable(TubeGL, self.engine.load_tubes, path, *args, **kwargs)
