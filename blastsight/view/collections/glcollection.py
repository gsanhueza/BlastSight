#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from collections import OrderedDict
from ..glprograms.shaderprogram import ShaderProgram
from ..drawables.gldrawable import GLDrawable


class GLCollection:
    def __init__(self):
        self._programs = OrderedDict()
        self._collection = OrderedDict()
        self._needs_update = True
        self._is_initialized = False

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
    def initialize(self) -> None:
        if self._is_initialized:
            return

        self.generate_associations()
        self.initialize_programs()
        self.update_drawables(include_hidden=True)

        self._is_initialized = True

    def generate_associations(self):
        pass

    def initialize_programs(self):
        for program in self.all_programs():
            program.initialize()

    def associate(self, program: ShaderProgram, d_type: type, selector: callable = lambda x: True) -> None:
        self._programs[program.class_name] = {
            'program': program,
            'type': d_type,
            'selector': selector,
        }

    def recreate(self) -> None:
        self._needs_update = True

    def get_program(self, program_name: str) -> ShaderProgram:
        return self._programs.get(program_name).get('program')

    def all_programs(self) -> list:
        return list(map(lambda x: x.get('program'), self.all_associations()))

    def all_associations(self) -> list:
        return list(self._programs.values())

    def update_drawables(self, include_hidden: bool = False) -> None:
        # Update shader program so that it knows what to draw
        for association in self.all_associations():
            program = association.get('program')
            drawable_type = association.get('type')
            selector = association.get('selector')

            drawables = self.select(drawable_type, selector)
            visibles = list(filter(lambda x: x.is_visible or include_hidden, drawables))
            program.set_drawables(visibles)

    def update_uniform(self, uniform: str, *values) -> None:
        for program in self.all_programs():
            program.update_uniform(uniform, *values)

    def update_custom_uniform(self, program_name: str, uniform: str, *values) -> None:
        program = self.get_program(program_name)
        program.update_uniform(uniform, *values)

    """
    Drawing methods
    """
    def draw_opaques(self) -> None:
        for program in self.all_programs():
            if len(program.opaques) > 0:
                program.bind()
                program.draw()

    def draw_transparents(self) -> None:
        for program in self.all_programs():
            if len(program.transparents) > 0:
                program.bind()
                program.redraw()

    def draw(self) -> None:
        # Try to update drawables if anyone changes
        if self._needs_update:
            self.update_drawables()
            self._needs_update = False

        self.draw_opaques()
        self.draw_transparents()
