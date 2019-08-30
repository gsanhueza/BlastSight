#!/usr/bin/env python

from collections import OrderedDict
from .gldrawable import GLDrawable


class GLCollection(OrderedDict):
    def __init__(self):
        super().__init__()
        self.programs = OrderedDict()

    def add(self, drawable: GLDrawable) -> None:
        self[drawable.id] = drawable

    def delete(self, id_: int) -> None:
        self[id_].cleanup()
        del self[id_]

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        for gl_program, lambda_drawables in self.programs.items():
            gl_program.setup()
            gl_program.bind()

            gl_program.update_uniform('proj_matrix', proj_matrix)
            gl_program.update_uniform('model_view_matrix', view_matrix * model_matrix)
            gl_program.set_drawables(lambda_drawables())
            gl_program.draw()

    def filter(self, drawable_type):
        return [x for x in self.values() if isinstance(x, drawable_type)]

    @property
    def last_id(self):
        # bool(dict) evaluates to False if the dictionary is empty
        return list(self.keys())[-1] if bool(self) else -1
