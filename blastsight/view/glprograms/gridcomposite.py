#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .shaderprogram import ShaderProgram
from .gridprogram import GridProgram
from .textprogram import TextProgram

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

    def generate_shaders(self) -> list:
        self.grid_program.generate_shaders()
        self.text_program.generate_shaders()

        return []

    def link_shaders(self) -> None:
        self.grid_program.link_shaders()
        self.text_program.link_shaders()

    def update_uniform(self, loc_str, *values) -> None:
        self.grid_program.update_uniform(loc_str, *values)
        self.text_program.update_uniform(loc_str, *values)

    def set_drawables(self, drawables: list) -> None:
        # WARNING Input only contains GridGL, but this is needed, or GLCollection will skip
        # this program (composite) if it doesn't see drawables inside!
        super().set_drawables(drawables)

        if len(drawables) == 0:
            return

        # When setting the Grid drawable, we can only assume one is selected
        # WARNING Remember that this is only a workaround for the current architecture!!!
        grid = drawables[-1]
        min_bound, max_bound = grid.bounding_box
        scale = 0.02 * max(1, np.sqrt(grid.mark_separation))

        text_drawables = []

        # Labels in X
        # Remember to separate the number text from the grid
        for x in grid.x_divisions:
            pos = int(min_bound[0] + x)
            textgl = TextGL(NullElement(), text=f'{pos}', position=[pos, min_bound[1] - 2.0, min_bound[2]], scale=scale)
            text_drawables.append(textgl)

        # Labels in Y
        for y in grid.y_divisions:
            pos = int(min_bound[1] + y)
            textgl = TextGL(NullElement(), text=f'{pos}', position=[min_bound[0] - 2.0, pos, min_bound[2] - 2.0], scale=scale)
            text_drawables.append(textgl)

        # Labels in Z
        for z in grid.z_divisions:
            pos = int(min_bound[2] + z)
            textgl = TextGL(NullElement(), text=f'{pos}', position=[min_bound[0] - 2.0, min_bound[1], pos], scale=scale)
            text_drawables.append(textgl)

        self.grid_program.set_drawables(drawables)
        self.text_program.set_drawables(text_drawables)

    def bind(self) -> None:
        pass

    def inner_draw(self, drawables: list) -> None:
        self.grid_program.bind()
        self.grid_program.inner_draw(self.grid_program.drawables)

        self.text_program.bind()
        self.text_program.inner_draw(self.text_program.drawables)
