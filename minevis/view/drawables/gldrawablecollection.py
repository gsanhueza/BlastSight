#!/usr/bin/env python

from collections import OrderedDict

from .gldrawable import GLDrawable
from .meshgl import MeshGL
from .blockgl import BlockGL
from .linegl import LineGL
from .pointgl import PointGL
from .tubegl import TubeGL
from .backgroundgl import BackgroundGL
from .axisgl import AxisGL

from .glprograms.meshprogram import MeshProgram
from .glprograms.wireframeprogram import WireframeProgram
from .glprograms.blockprogram import BlockProgram
from .glprograms.lineprogram import LineProgram
from .glprograms.pointprogram import PointProgram
from .glprograms.tubeprogram import TubeProgram
from .glprograms.backgroundprogram import BackgroundProgram
from .glprograms.axisprogram import AxisProgram


class GLDrawableCollection(OrderedDict):
    def __init__(self, widget=None):
        super().__init__()
        self.programs = OrderedDict()

        self.programs['bg'] = BackgroundProgram(widget), (lambda: self.background)
        self.programs['axis'] = AxisProgram(widget), (lambda: self.axis)
        self.programs['blockmodel'] = BlockProgram(widget), (lambda: self.block_models)
        self.programs['line'] = LineProgram(widget), (lambda: self.lines)
        self.programs['tube'] = TubeProgram(widget), (lambda: self.tubes)
        self.programs['point'] = PointProgram(widget), (lambda: self.points)
        self.programs['mesh'] = MeshProgram(widget), (lambda: self.normal_meshes)
        self.programs['wireframe'] = WireframeProgram(widget), (lambda: self.wireframe_meshes)

    def add(self, drawable: GLDrawable) -> None:
        self[drawable.id] = drawable

    def delete(self, id_: int) -> None:
        self[id_].cleanup()
        del self[id_]

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        for k, v in self.programs.items():
            self.programs[k][0].setup()
            self.programs[k][0].bind()

            self.programs[k][0].update_uniform('proj_matrix', proj_matrix)
            self.programs[k][0].update_uniform('model_view_matrix', view_matrix * model_matrix)
            self.programs[k][0].set_drawables(self.programs[k][1]())
            self.programs[k][0].draw()

    def filter(self, drawable_type):
        return list(filter(lambda x: isinstance(x, drawable_type), super().values()))

    def keys(self):
        return filter(lambda x: isinstance(x, int), super().keys())

    def items(self):
        return filter(lambda x: isinstance(x[0], int), super().items())

    def values(self):
        return filter(lambda x: isinstance(x.id, int), super().values())

    def __len__(self):
        return list(self.items()).__len__()

    @property
    def last_id(self):
        try:
            return list(self.items())[-1][0]
        except IndexError:
            return -1

    @property
    def background(self):
        return self.filter(BackgroundGL)

    @property
    def axis(self):
        return self.filter(AxisGL)

    @property
    def meshes(self):
        return self.filter(MeshGL)

    @property
    def normal_meshes(self):
        return list(filter(lambda x: not x.wireframe_enabled, self.meshes))

    @property
    def wireframe_meshes(self):
        return list(filter(lambda x: x.wireframe_enabled, self.meshes))

    @property
    def block_models(self):
        return self.filter(BlockGL)

    @property
    def points(self):
        return self.filter(PointGL)

    @property
    def lines(self):
        return self.filter(LineGL)

    @property
    def tubes(self):
        return self.filter(TubeGL)
