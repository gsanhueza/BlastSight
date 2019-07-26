#!/usr/bin/env python

from collections import OrderedDict

from .gldrawable import GLDrawable
from .meshgl import MeshGL
from .blockmodelgl import BlockModelGL
from .linegl import LineGL
from .pointgl import PointGL
from .tubegl import TubeGL
from .backgroundgl import BackgroundGL
from .axisgl import AxisGL

from .meshprogram import MeshProgram
from .wireframeprogram import WireframeProgram
from .blockmodelprogram import BlockModelProgram
from .lineprogram import LineProgram
from .pointprogram import PointProgram
from .tubeprogram import TubeProgram
from .backgroundprogram import BackgroundProgram
from .axisprogram import AxisProgram


class GLDrawableCollection(OrderedDict):
    def __init__(self, widget=None):
        super().__init__()
        self.programs = OrderedDict()

        self.programs['mesh'] = MeshProgram(widget)
        self.programs['wireframe'] = WireframeProgram(widget)
        self.programs['blockmodel'] = BlockModelProgram(widget)
        self.programs['line'] = LineProgram(widget)
        self.programs['point'] = PointProgram(widget)
        self.programs['tube'] = TubeProgram(widget)
        self.programs['bg'] = BackgroundProgram(widget)
        self.programs['axis'] = AxisProgram(widget)

    def add(self, drawable: GLDrawable) -> None:
        self[drawable.id] = drawable

    def delete(self, id_: int) -> None:
        del self[id_]

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        types = OrderedDict()

        types['bg'] = self.background
        types['axis'] = self.axis
        types['tube'] = self.tubes
        types['wireframe'] = self.wireframe_meshes
        types['line'] = self.lines
        types['point'] = self.points
        types['mesh'] = self.normal_meshes
        types['blockmodel'] = self.block_models

        for k, v in types.items():
            self.programs[k].setup()
            self.programs[k].bind()

            self.programs[k].update_uniform('proj_matrix', proj_matrix)
            self.programs[k].update_uniform('model_view_matrix', view_matrix * model_matrix)
            self.programs[k].set_drawables(v)
            self.programs[k].draw()

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
        return self.filter(BlockModelGL)

    @property
    def points(self):
        return self.filter(PointGL)

    @property
    def lines(self):
        return self.filter(LineGL)

    @property
    def tubes(self):
        return self.filter(TubeGL)
