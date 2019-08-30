#!/usr/bin/env python

from qtpy.QtGui import QOpenGLShader
from .shaderprogram import ShaderProgram
from OpenGL.GL import *


class MeshProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)

    def setup_shaders(self):
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)

        vertex_shader.compileSourceFile(f'{self.shader_dir}/Mesh/vertex.glsl')
        fragment_shader.compileSourceFile(f'{self.shader_dir}/Mesh/fragment.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()

    def draw(self):
        wireframed = []
        normal = []
        normal_opaque = []
        normal_glass = []

        for drawable in self.drawables:
            wireframed.append(drawable) if drawable.wireframe_enabled else normal.append(drawable)

        for drawable in normal:
            normal_opaque.append(drawable) if drawable.element.alpha >= 0.99 else normal_glass.append(drawable)

        # Opaque/Wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for drawable in wireframed:
            drawable.draw()

        # Opaque/Normal
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        for drawable in normal_opaque:
            drawable.draw()

        # Transparent/Normal
        for drawable in normal_glass:
            drawable.draw()
