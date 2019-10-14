#!/usr/bin/env python

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
        for gl_program, lambda_drawables in self.programs.items():
            if self.needs_update:
                drawables = lambda_drawables()
                gl_program.set_drawables(drawables)
                if len(drawables) == 0:
                    continue

            gl_program.setup()
            gl_program.bind()

            gl_program.update_uniform('proj_matrix', proj_matrix)
            gl_program.update_uniform('model_view_matrix', view_matrix * model_matrix)
            gl_program.draw()

        self.needs_update = False

    def filter(self, drawable_type: type) -> list:
        # The copy avoids RuntimeError: OrderedDict mutated during iteration
        try:
            return [x for x in self.values() if type(x) is drawable_type]
        except RuntimeError:
            return [x for x in self.copy().values() if type(x) is drawable_type]

    @property
    def last_id(self):
        # bool(dict) evaluates to False if the dictionary is empty
        return list(self.keys())[-1] if bool(self) else -1
