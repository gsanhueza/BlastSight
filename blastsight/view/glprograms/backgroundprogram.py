#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram


class BackgroundProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Background'

    def setup(self) -> None:
        super().setup()
        self.add_uniform_loc('top_color')
        self.add_uniform_loc('bot_color')

    def inner_draw(self, drawables):
        for drawable in drawables:
            self.update_uniform('top_color', *drawable.top_color)
            self.update_uniform('bot_color', *drawable.bot_color)
            drawable.draw()
