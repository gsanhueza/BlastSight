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

        # Labels in X
        # Remember to separate the number text from the grid
        x_marks = grid.x_ticks.tolist()
        y_marks = grid.y_ticks.tolist()
        z_marks = grid.z_ticks.tolist()

        # What the text says shall be known beforehand
        matrix = grid.calculate_rotation_matrix()

        x_text = np.round(list(map(lambda mark: GridGL.rotate_mark_with_qmatrix(matrix, mark), x_marks)), 4)
        y_text = np.round(list(map(lambda mark: GridGL.rotate_mark_with_qmatrix(matrix, mark), y_marks)), 4)
        z_text = np.round(list(map(lambda mark: GridGL.rotate_mark_with_qmatrix(matrix, mark), z_marks)), 4)

        # Setup scale of the text
        all_divisions = np.append(np.append(x_marks, y_marks), z_marks)
        max_width = max(map(lambda i: len(str(i)), all_divisions))
        scale = grid.mark_separation / np.sqrt(max_width)

        for rel_pos, rel_text in zip(x_marks, x_text):
            pos = grid.origin + rel_pos
            text = grid.origin + rel_text

            textgl = TextGL(NullElement(), text=f'{text[0]}', scale=scale, centered=False,
                            rotation=[0.0, 0.0, 90.0], color=grid.text_color,
                            position=pos)

            # Ensure text doesn't overlap with grid
            textgl.initialize()
            tvs = textgl.text_vertices.reshape((-1, 3))
            ptp = np.ptp(tvs, axis=0)
            tvs -= [-ptp[0] / 2, ptp[1] + scale, 0.0]
            textgl.text_vertices = tvs.reshape((len(textgl.text), -1))

            text_drawables.append(textgl)

        # Labels in Y
        for rel_pos, rel_text in zip(y_marks, y_text):
            pos = grid.origin + rel_pos
            text = grid.origin + rel_text

            textgl = TextGL(NullElement(), text=f'{text[1]}', scale=scale, centered=False,
                            rotation=[0.0, 0.0, 0.0], color=grid.text_color,
                            position=pos)

            # Ensure text doesn't overlap with grid
            textgl.initialize()
            tvs = textgl.text_vertices.reshape((-1, 3))
            ptp = np.ptp(tvs, axis=0)
            tvs -= [ptp[0] + scale, ptp[1] / 2, 0.0]
            textgl.text_vertices = tvs.reshape((len(textgl.text), -1))

            text_drawables.append(textgl)

        # Labels in Z
        for rel_pos, rel_text in zip(z_marks, z_text):
            pos = grid.origin + rel_pos
            text = grid.origin + rel_text

            textgl = TextGL(NullElement(), text=f'{text[2]}', scale=scale, centered=False,
                            rotation=[90.0, 0.0, 0.0], color=grid.text_color,
                            position=pos)

            # Ensure text doesn't overlap with grid
            textgl.initialize()
            tvs = textgl.text_vertices.reshape((-1, 3))
            ptp = np.ptp(tvs, axis=0)
            tvs -= [ptp[0] + scale, 0.0, ptp[2] / 2]
            textgl.text_vertices = tvs.reshape((len(textgl.text), -1))

            text_drawables.append(textgl)

        # Finally, make the text rotation
        for textgl in text_drawables:
            final_vertices = list()
            for vertices in textgl.text_vertices:
                quad = vertices.reshape((-1, 3))
                rotated_quad = np.array(list(map(lambda v: GridGL.rotate_mark_with_qmatrix(matrix, v), quad)))
                final_vertices.append(rotated_quad.reshape(-1))

            textgl.text_vertices = np.array(final_vertices, np.float32)
            textgl.initialize()

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
