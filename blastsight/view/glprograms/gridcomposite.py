#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from OpenGL.GL import *

from .shaderprogram import ShaderProgram
from .gridprogram import GridProgram
from .textprogram import TextProgram

from ..drawables.gridgl import GridGL
from ..drawables.textgl import TextGL
from ...model.elements.nullelement import NullElement


class GridComposite(ShaderProgram):
    """
    This is a composite program, that needs two shader programs to work,
    because we need to render both lines (grid) and triangles (grid text).
    """

    def __init__(self):
        super().__init__()
        self.grid_program = GridProgram()
        self.text_program = TextProgram()

    def initialize(self) -> None:
        self.grid_program.initialize()
        self.text_program.initialize()

    def update_uniform(self, loc_str, *values) -> None:
        self.grid_program.update_uniform(loc_str, *values)
        self.text_program.update_uniform(loc_str, *values)

    @staticmethod
    def generate_labels(grid: GridGL) -> list:
        text_drawables = []

        min_bound, max_bound = grid.bounding_box
        all_divisions = grid.x_divisions.tolist() + grid.y_divisions.tolist() + grid.z_divisions.tolist()
        max_width = max(map(lambda i: len(str(int(i))), all_divisions))

        scale = grid.mark_separation / max_width

        # Labels in X
        # Remember to separate the number text from the grid
        for x in grid.x_divisions:
            pos = int(min_bound[0] + x)
            textgl = TextGL(NullElement(), text=f'{pos}', scale=scale, centered=False,
                            rotation=[0.0, 0.0, 90.0], color=grid.text_color,
                            position=[pos, min_bound[1], min_bound[2]])

            # Ensure text doesn't overlap with grid
            textgl.initialize()
            tvs = textgl.text_vertices.reshape((-1, 3))
            ptp = np.ptp(tvs, axis=0)
            tvs -= [-ptp[0] / 2, ptp[1] + scale, 0.0]
            textgl.text_vertices = tvs.reshape((len(textgl.text), -1))

            text_drawables.append(textgl)

        # Labels in Y
        for y in grid.y_divisions:
            pos = int(min_bound[1] + y)
            textgl = TextGL(NullElement(), text=f'{pos}', scale=scale, centered=False,
                            rotation=[0.0, 0.0, 0.0], color=grid.text_color,
                            position=[min_bound[0], pos, min_bound[2]])

            # Ensure text doesn't overlap with grid
            textgl.initialize()
            tvs = textgl.text_vertices.reshape((-1, 3))
            ptp = np.ptp(tvs, axis=0)
            tvs -= [ptp[0] + scale, ptp[1] / 2, 0.0]
            textgl.text_vertices = tvs.reshape((len(textgl.text), -1))

            text_drawables.append(textgl)

        # Labels in Z
        for z in grid.z_divisions:
            pos = int(min_bound[2] + z)
            textgl = TextGL(NullElement(), text=f'{pos}', scale=scale, centered=False,
                            rotation=[90.0, 0.0, 0.0], color=grid.text_color,
                            position=[min_bound[0], min_bound[1], pos])

            # Ensure text doesn't overlap with grid
            textgl.initialize()
            tvs = textgl.text_vertices.reshape((-1, 3))
            ptp = np.ptp(tvs, axis=0)
            tvs -= [ptp[0] + scale, 0.0, ptp[2] / 2]
            textgl.text_vertices = tvs.reshape((len(textgl.text), -1))

            text_drawables.append(textgl)

        return text_drawables

    def set_drawables(self, drawables: list) -> None:
        def flatten(t):
            return [item for sublist in t for item in sublist]

        # WARNING Input only contains GridGL, but this is needed, or GLCollection will skip
        # this program (composite) if it doesn't see drawables inside!
        super().set_drawables(drawables)
        all_text_drawables = flatten(map(self.generate_labels, drawables))

        self.grid_program.set_drawables(drawables)
        self.text_program.set_drawables(all_text_drawables)

    def bind(self) -> None:
        pass

    def inner_draw(self, drawables: list) -> None:
        glDisable(GL_DEPTH_TEST)

        self.grid_program.bind()
        self.grid_program.inner_draw(self.grid_program.drawables)

        self.text_program.bind()
        self.text_program.inner_draw(self.text_program.drawables)

        glEnable(GL_DEPTH_TEST)
