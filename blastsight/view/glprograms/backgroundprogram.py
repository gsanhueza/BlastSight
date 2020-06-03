#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram


class BackgroundProgram(ShaderProgram):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.base_name = 'Background'

    def initialize(self) -> None:
        super().initialize()
        self.add_uniform_loc('top_color')
        self.add_uniform_loc('bottom_color')

    def inner_draw(self, drawables: list) -> None:
        for drawable in drawables:
            self.update_uniform('top_color', *drawable.top_color)
            self.update_uniform('bottom_color', *drawable.bottom_color)
            drawable.draw()
