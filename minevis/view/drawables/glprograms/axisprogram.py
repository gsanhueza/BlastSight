#!/usr/bin/env python

from OpenGL.GL import glViewport
from .shaderprogram import ShaderProgram


class AxisProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Axis'

    def draw(self):
        viewport = [self.widget.devicePixelRatio() * self.widget.width(),
                    self.widget.devicePixelRatio() * self.widget.height()]
        w, h = viewport

        glViewport(w // 20, h // 20, h // 6, h // 6)
        super().draw()
        glViewport(0, 0, viewport[0], viewport[1])
