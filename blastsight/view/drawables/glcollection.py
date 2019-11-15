#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from collections import OrderedDict
from .gldrawable import GLDrawable


class GLCollection(OrderedDict):
    def __init__(self):
        super().__init__()
        self.programs = OrderedDict()
        self.needs_update = True

    def add(self, drawable: GLDrawable) -> None:
        self[drawable.id] = drawable

    def delete(self, _id: int) -> None:
        self[_id].cleanup()
        del self[_id]

    def recreate(self):
        self.needs_update = True
        for gl_program in self.programs.keys():
            gl_program.recreate()

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        # Update shader program so that it knows what to draw.
        if self.needs_update:
            for gl_program, lambda_drawables in self.programs.items():
                # Get the meshes that we'll really render
                drawables = [d for d in lambda_drawables() if d.is_visible]
                gl_program.set_drawables(drawables)
            self.needs_update = False

        for gl_program, lambda_drawables in self.programs.items():
            # Skip bindings if there are no elements of this type.
            if len(gl_program.drawables) == 0:
                continue

            gl_program.setup()
            gl_program.bind()

            gl_program.update_uniform('proj_matrix', proj_matrix)
            gl_program.update_uniform('model_view_matrix', view_matrix * model_matrix)
            gl_program.draw()

    def filter(self, drawable_type: type) -> list:
        # The copy avoids RuntimeError: OrderedDict mutated during iteration
        return [x for x in self.copy().values() if type(x) is drawable_type]

    @property
    def last_id(self):
        # bool(dict) evaluates to False if the dictionary is empty
        return list(self.keys())[-1] if bool(self) else -1
