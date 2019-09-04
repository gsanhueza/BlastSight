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
            # We need DPI awareness for the size of the impostors
            viewport = [self.widget.devicePixelRatio() * self.widget.width(),
                        self.widget.devicePixelRatio() * self.widget.height()]
            self.update_uniform('viewport', *viewport)
            self.update_uniform('marker', drawable.element.marker)
            drawable.draw()
