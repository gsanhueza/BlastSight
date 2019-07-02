#!/usr/bin/env python

from collections import OrderedDict

from .gldrawable import GLDrawable
from .meshgl import MeshGL
from .blockmodelgl import BlockModelGL
from .linegl import LineGL
from .pointgl import PointGL
from .tubegl import TubeGL

from .meshprogram import MeshProgram
from .wireframeprogram import WireframeProgram
from .blockmodelprogram import BlockModelProgram
from .lineprogram import LineProgram
from .pointprogram import PointProgram
from .tubeprogram import TubeProgram


class GLDrawableCollection(OrderedDict):
    def __init__(self, widget=None):
        super().__init__()
        self.programs = {
            'mesh': MeshProgram(widget),
            'wireframe': WireframeProgram(widget),
            'blockmodel': BlockModelProgram(widget),
            'line': LineProgram(widget),
            'point': PointProgram(widget),
            'tube': TubeProgram(widget),
        }

    def add(self, id_: int, drawable: GLDrawable) -> None:
        self.__setitem__(id_, drawable)

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        types = {
            'mesh': self.normal_meshes,
            'wireframe': self.wireframe_meshes,
            'blockmodel': self.block_models,
            'line': self.lines,
            'point': self.points,
            'tube': self.tubes,
        }

        for k, v in types.items():
            self.programs[k].setup()
            self.programs[k].bind()

            self.programs[k].update_uniform('proj_matrix', proj_matrix)
            self.programs[k].update_uniform('model_view_matrix', view_matrix * model_matrix)
            self.programs[k].set_drawables(v)
            self.programs[k].draw()

    def filter(self, drawable_type):
        return list(filter(lambda x: isinstance(x, drawable_type), self.values()))

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
