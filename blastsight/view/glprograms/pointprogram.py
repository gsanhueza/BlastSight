#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram


class PointProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'Point'

    def initialize(self) -> None:
        super().initialize()
        self.add_uniform_handler('viewport')
        self.add_uniform_handler('marker')

    def inner_draw(self, drawables: list) -> None:
        for drawable in drawables:
            self.update_uniform('marker', drawable.element.marker_num)
            drawable.draw()
