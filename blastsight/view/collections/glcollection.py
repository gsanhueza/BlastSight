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

    def get_all_ids(self) -> list:
        return list(self._collection.keys())

    def get_all_drawables(self) -> list:
        return list(self._collection.values())

    def delete(self, _id: int) -> None:
        drawable = self._collection.pop(_id)
        drawable.cleanup()

    def clear(self) -> None:
        self._collection.clear()

    def size(self) -> int:
        return len(self._collection)

    def filter(self, drawable_type: type) -> list:
        # The copy avoids RuntimeError: OrderedDict mutated during iteration
        return [x for x in self._collection.copy().values() if type(x) is drawable_type]

    def retrieve(self, drawable_type: type, required: str = 'all') -> callable:
        runner = {
            'all': lambda x: True,
            'mesh_standard': lambda x: not (x.is_turbo_ready or x.is_wireframed),
            'mesh_turbo': lambda x: x.is_turbo_ready,
            'mesh_wireframe': lambda x: x.is_wireframed,
            'block_legacy': lambda x: x.is_legacy,
            'block_standard': lambda x: not x.is_legacy,
        }

        return list(filter(runner.get(required), self.filter(drawable_type)))

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

    def associate(self, program: ShaderProgram, retriever: callable) -> None:
        self._programs[program.get_base_name()] = {
            'program': program,
            'retriever': retriever,
        }

    def recreate(self) -> None:
        self._needs_update = True

    def get_programs(self) -> list:
        return [x.get('program') for x in self._programs.values()]

    def get_retrievers(self) -> list:
        return [x.get('retriever') for x in self._programs.values()]

    def update_drawables(self) -> None:
        # Update shader program so that it knows what to draw
        # FIXME Can we modify this method to not need self._needs_update ?
        if self._needs_update:
            for association in self._programs.values():
                program = association.get('program')
                retriever = association.get('retriever')
                program.set_drawables([d for d in retriever() if d.is_visible])
            self._needs_update = False

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
        list(map(bind_update, self.get_programs()))

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
        self.update_drawables()
        self.update_uniforms()
        self.draw_opaques()
        self.draw_transparents()
