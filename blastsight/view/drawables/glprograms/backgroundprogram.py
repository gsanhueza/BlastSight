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
        self.color_set = False

    def setup(self) -> None:
        super().setup()
        self.add_uniform_loc('top_color')
        self.add_uniform_loc('bot_color')

    def draw(self):
        if not self.color_set:
            self.update_uniform('top_color', 0.1, 0.2, 0.3, 1.0)
            self.update_uniform('bot_color', 0.4, 0.5, 0.6, 1.0)
            self.color_set = True
        super().draw()
