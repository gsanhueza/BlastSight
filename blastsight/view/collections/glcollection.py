#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from collections import OrderedDict
from ..glprograms.shaderprogram import ShaderProgram
from ..drawables.gldrawable import GLDrawable


class GLCollection:
    def __init__(self, viewer=None):
        self._viewer = viewer
        self._programs = OrderedDict()
        self._collection = OrderedDict()
        self._uniform_data = {}
        self._needs_update = True

    """
    Drawable collection handlers
    """
    def add(self, drawable: GLDrawable) -> None:
        self._collection[drawable.id] = drawable
        self._needs_update = True

    def get(self, _id: int) -> GLDrawable:
        return self._collection.get(_id)

    def get_last(self) -> GLDrawable:
        return self.get(self.last_id)

    def all_ids(self) -> list:
        return list(self._collection.keys())

    def all_drawables(self) -> list:
        # The copy avoids RuntimeError: OrderedDict mutated during iteration
        return list(self._collection.copy().values())

    def delete(self, _id: int) -> None:
        drawable = self._collection.pop(_id)
        drawable.cleanup()

    def clear(self) -> None:
        self._collection.clear()

    def size(self) -> int:
        return len(self._collection)

    def select(self, drawable_type: type, selector: callable = lambda x: True) -> list:
        # Filters by type
        def matches_type(x) -> bool:
            return type(x) is drawable_type

        # Filters by type and selector
        def matches_all(x) -> bool:
            return matches_type(x) and selector(x)

        return list(filter(matches_all, self.all_drawables()))

    @property
    def last_id(self) -> int:
        # bool(dict) evaluates to False if the dictionary is empty
        return list(self._collection.keys())[-1] if bool(self._collection) else -1

    """
    ShaderProgram collection handlers
    """
    # FIXME We could have a collection handler, so every method from here and below
    #  could be in the GLCollectionHandler, instead of in a collection
    def initialize(self) -> None:
        for program in self.get_programs():
            program.initialize()

    def associate(self, program: ShaderProgram, d_type: type, selector: callable = lambda x: True) -> None:
        self._programs[program.get_base_name()] = {
            'program': program,
            'type': d_type,
            'selector': selector,
        }

    def recreate(self) -> None:
        self._needs_update = True

    def get_programs(self) -> list:
        return list(map(lambda x: x.get('program'), self._programs.values()))

    def update_drawables(self) -> None:
        # Update shader program so that it knows what to draw
        for association in self._programs.values():
            program = association.get('program')
            drawable_type = association.get('type')
            selector = association.get('selector')

            drawables = self.select(drawable_type, selector)
            visibles = list(filter(lambda x: x.is_visible, drawables))
            program.set_drawables(visibles)

    def update_matrix(self, matrix: str, value) -> None:
        self._uniform_data[matrix] = value

    def update_uniform(self, program_name: str, uniform: str, *values) -> None:
        program = self._programs.get(program_name).get('program')
        program.update_uniform(uniform, *values)

    def update_uniforms(self) -> None:
        # Update matrices so that it knows where it's looking
        def bind_update(prog):
            prog.bind()
            for k, v in self._uniform_data.items():
                prog.update_uniform(k, v)

        # Apply to each program
        for program in self.get_programs():
            bind_update(program)

    """
    Drawing methods
    """
    def draw_opaques(self) -> None:
        for program in self.get_programs():
            if len(program.opaques) > 0:
                program.bind()
                program.draw()

    def draw_transparents(self) -> None:
        for program in self.get_programs():
            if len(program.transparents) > 0:
                program.bind()
                program.redraw()

    def draw(self) -> None:
        # Try to update drawables if anyone changes
        if self._needs_update:
            self.update_drawables()
            self._needs_update = False

        self.update_uniforms()
        self.draw_opaques()
        self.draw_transparents()
