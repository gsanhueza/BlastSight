#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from collections import OrderedDict
from .glprogramcollection import GLProgramCollection
from ..drawables.gldrawable import GLDrawable


class GLCollection:
    def __init__(self, viewer=None):
        self._viewer = viewer
        self._programs = GLProgramCollection()
        self._collection = OrderedDict()
        self.needs_update = True

    """
    Drawable collection handlers
    """
    def add(self, drawable: GLDrawable) -> None:
        self._collection[drawable.id] = drawable
        self.needs_update = True

    def get(self, _id: int) -> GLDrawable:
        return self._collection.get(_id)

    def get_all_ids(self) -> list:
        return list(self._collection.keys())

    def get_all_drawables(self) -> list:
        return list(self._collection.values())

    def delete(self, _id: int) -> None:
        drawable = self._collection.pop(_id)
        drawable.cleanup()

    def filter(self, drawable_type: type) -> list:
        # The copy avoids RuntimeError: OrderedDict mutated during iteration
        return [x for x in self._collection.copy().values() if type(x) is drawable_type]

    def clear(self) -> None:
        self._collection.clear()

    def size(self) -> int:
        return len(self._collection)

    @property
    def last_id(self) -> int:
        # bool(dict) evaluates to False if the dictionary is empty
        return list(self._collection.keys())[-1] if bool(self._collection) else -1

    """
    ShaderProgram collection handlers
    """
    def associate(self, program, association) -> None:
        """
        :param program: AxisProgram, for example
        :param association: lambda
        :return: None
        """
        self._programs.associate(program, association)

    def recreate(self) -> None:
        self.needs_update = True
        for program in self._programs.get_programs():
            program.recreate()

    def update_drawables(self) -> None:
        # Update shader program so that it knows what to draw
        if self.needs_update:
            for program, drawable_retriever in self._programs.get_pairs():
                program.set_drawables([d for d in drawable_retriever() if d.is_visible])
            self.needs_update = False

    def update_matrices(self, proj, view, model) -> None:
        # Update matrices so that it knows where it's looking
        for program in self._programs.get_programs():
            if len(program.drawables) > 0:
                program.setup()
                program.bind()
                program.update_uniform('proj_matrix', proj)
                program.update_uniform('model_view_matrix', view * model)

    """
    Drawing methods
    """
    def draw_opaques(self) -> None:
        for program in self._programs.get_programs():
            if len(program.opaques) > 0:
                program.bind()
                program.draw()

    def draw_transparents(self) -> None:
        for program in self._programs.get_programs():
            if len(program.transparents) > 0:
                program.bind()
                program.redraw()

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        self.update_drawables()
        self.update_matrices(proj_matrix, view_matrix, model_matrix)
        self.draw_opaques()
        self.draw_transparents()
