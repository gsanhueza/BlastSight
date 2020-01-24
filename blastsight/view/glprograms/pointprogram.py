#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram


class PointProgram(ShaderProgram):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.base_name = 'Point'

    def setup(self) -> None:
        super().setup()
        self.add_uniform_loc('viewport')
        self.add_uniform_loc('marker')

    def inner_draw(self, drawables: list) -> None:
        for drawable in drawables:
            # We need DPI awareness for the size of the impostors
            viewport = [float(self.viewer.devicePixelRatio() * self.viewer.width()),
                        float(self.viewer.devicePixelRatio() * self.viewer.height())]
            self.update_uniform('viewport', *viewport)
            self.update_uniform('marker', drawable.element.marker_num)
            drawable.draw()
