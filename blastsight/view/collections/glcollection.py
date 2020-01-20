#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from collections import OrderedDict
from ..drawables.gldrawable import GLDrawable


class GLCollection:
    def __init__(self):
        super().__init__()
        self._programs = OrderedDict()
        self._collection = OrderedDict()
        self._needs_update = True

    def add(self, drawable: GLDrawable) -> None:
        self._collection[drawable.id] = drawable
        self._needs_update = True

    def get(self, _id: int) -> GLDrawable:
        return self._collection.get(_id)

    def get_all_ids(self) -> list:
        return list(self._collection.keys())

    def get_all_drawables(self) -> list:
        return list(self._collection.values())

    def update(self, _id: int, drawable: GLDrawable) -> None:
        self._collection[_id] = drawable
        self._needs_update = True

    def delete(self, _id: int) -> None:
        drawable = self._collection.pop(_id)
        drawable.cleanup()

    def clear(self) -> None:
        self._collection.clear()

    def size(self) -> int:
        return len(self._collection)

    def recreate(self):
        self._needs_update = True
        for gl_program in self._programs.keys():
            gl_program.recreate()

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        # Update shader program so that it knows what to draw.
        if self._needs_update:
            for gl_program, lambda_drawables in self._programs.items():
                # Get the meshes that we'll really render
                gl_program.set_drawables([d for d in lambda_drawables() if d.is_visible])
            self._needs_update = False

        def inner_draw(programs, collection, method):
            for program in programs:
                if len(getattr(program, collection)) == 0:
                    continue

                program.setup()
                program.bind()

                program.update_uniform('proj_matrix', proj_matrix)
                program.update_uniform('model_view_matrix', view_matrix * model_matrix)

                getattr(program, method)()

        inner_draw(self._programs.keys(), collection='drawables', method='draw')
        inner_draw(self._programs.keys(), collection='transparents', method='redraw')

    def filter(self, drawable_type: type) -> list:
        # The copy avoids RuntimeError: OrderedDict mutated during iteration
        return [x for x in self._collection.copy().values() if type(x) is drawable_type]

    @property
    def last_id(self):
        # bool(dict) evaluates to False if the dictionary is empty
        return list(self._collection.keys())[-1] if bool(self._collection) else -1
