#!/usr/bin/env python

from collections import OrderedDict

from qtpy.QtGui import QVector2D

from .gldrawable import GLDrawable
from .meshgl import MeshGL
from .blockmodelgl import BlockModelGL

from .meshprogram import MeshProgram
from .wireframeprogram import WireframeProgram
from .blockmodelprogram import BlockModelProgram


class GLDrawableCollection(OrderedDict):
    def __init__(self, widget):
        super().__init__()
        self.mesh_program = MeshProgram(widget)
        self.wireframe_program = WireframeProgram(widget)
        self.blockmodel_program = BlockModelProgram(widget)

    def add(self, id_: int, drawable: GLDrawable) -> None:
        self.__setitem__(id_, drawable)

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        # Meshes
        self.mesh_program.setup_program()
        self.mesh_program.bind()

        self.mesh_program.update_uniform('proj_matrix', proj_matrix)
        self.mesh_program.update_uniform('model_view_matrix', view_matrix * model_matrix)

        for drawable in self.normal_meshes:
            self.mesh_program.update_uniform('u_color', float(drawable.color[0]), float(drawable.color[1]), float(drawable.color[2]), drawable.alpha)
            drawable.draw()

        # Wireframe meshes
        self.wireframe_program.setup_program()
        self.wireframe_program.bind()

        self.wireframe_program.update_uniform('proj_matrix', proj_matrix)
        self.wireframe_program.update_uniform('model_view_matrix', view_matrix * model_matrix)

        for drawable in self.wireframe_meshes:
            self.wireframe_program.update_uniform('u_color', float(drawable.color[0]), float(drawable.color[1]), float(drawable.color[2]), drawable.alpha)

            drawable.draw()

        # Block Models
        self.blockmodel_program.setup_program()
        self.blockmodel_program.bind()

        self.blockmodel_program.update_uniform('proj_matrix', proj_matrix)
        self.blockmodel_program.update_uniform('model_view_matrix', view_matrix * model_matrix)

        for drawable in self.block_models:
            self.blockmodel_program.update_uniform('block_size', QVector2D(drawable.block_size, 0.0)),
            self.blockmodel_program.update_uniform('min_max', QVector2D(drawable.min_val, drawable.max_val)),

            drawable.draw()

        # Others
        for drawable in self.get_others():
            if not drawable.is_initialized:
                drawable.initialize()

            drawable.draw(proj_matrix, view_matrix, model_matrix)

    def filter(self, drawable_type):
        return list(filter(lambda x: isinstance(x, drawable_type), self.values()))

    def get_meshes(self):
        return self.filter(MeshGL)

    @property
    def normal_meshes(self):
        return list(filter(lambda x: not x.wireframe_enabled, self.filter(MeshGL)))

    @property
    def wireframe_meshes(self):
        return list(filter(lambda x: x.wireframe_enabled, self.filter(MeshGL)))

    @property
    def block_models(self):
        return self.filter(BlockModelGL)

    def get_others(self):
        return list(filter(lambda x: not isinstance(x, MeshGL) and not isinstance(x, BlockModelGL), self.values()))
