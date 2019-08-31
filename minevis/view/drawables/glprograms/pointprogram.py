#!/usr/bin/env python

from .shaderprogram import ShaderProgram


class PointProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Point'

    def setup(self) -> None:
        super().setup()
        self.add_uniform_loc('viewport')
        self.add_uniform_loc('marker')

    def draw(self):
        for drawable in self.drawables:
            self.update_uniform('viewport', self.widget.width(), self.widget.height())
            self.update_uniform('marker', drawable.element.marker)
            drawable.draw()
