#!/usr/bin/env python

from qtpy.QtGui import QOpenGLShader
from .shaderprogram import ShaderProgram


class PointProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)

    def setup(self) -> None:
        super().setup()
        self.add_uniform_loc('point_size')
        self.add_uniform_loc('viewport')
        self.add_uniform_loc('min_max')
        self.add_uniform_loc('marker')

    def setup_shaders(self):
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)

        vertex_shader.compileSourceFile(f'{self.shader_dir}/Point/vertex.glsl')
        fragment_shader.compileSourceFile(f'{self.shader_dir}/Point/fragment.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()

    def draw(self):
        for drawable in self.drawables:
            self.update_uniform('point_size', drawable.point_size)
            self.update_uniform('viewport', self.widget.width(), self.widget.height())
            self.update_uniform('min_max', drawable.min_val, drawable.max_val)
            self.update_uniform('marker', int(drawable.element.marker == 'circle'))
            drawable.draw()
