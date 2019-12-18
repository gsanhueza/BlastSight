#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from collections import OrderedDict
from ..drawables.gldrawable import GLDrawable


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
                gl_program.set_drawables([d for d in lambda_drawables() if d.is_visible])
            self.needs_update = False

        def inner_draw(programs, collection, method):
            for program in programs:
                if len(getattr(program, collection)) == 0:
                    continue

                program.setup()
                program.bind()

                program.update_uniform('proj_matrix', proj_matrix)
                program.update_uniform('model_view_matrix', view_matrix * model_matrix)

                getattr(program, method)()

        inner_draw(self.programs.keys(), collection='drawables', method='draw')
        inner_draw(self.programs.keys(), collection='transparents', method='redraw')

    def filter(self, drawable_type: type) -> list:
        # The copy avoids RuntimeError: OrderedDict mutated during iteration
        return [x for x in self.copy().values() if type(x) is drawable_type]

    @property
    def last_id(self):
        # bool(dict) evaluates to False if the dictionary is empty
        return list(self.keys())[-1] if bool(self) else -1
