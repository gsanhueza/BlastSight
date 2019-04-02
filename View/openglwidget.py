#!/usr/bin/env python

import numpy as np
import math

from OpenGL.GL import *
from PySide2.QtWidgets import QOpenGLWidget
from PySide2.QtGui import *
from PySide2.QtCore import Qt, Slot

from .normalmode import NormalMode

_POSITION = 0
_COLOR = 1


class OpenGLWidget(QOpenGLWidget):
    # FIXME We might not get a model every time. We need to have a fallback option to only receive vertices, for example
    def __init__(self, parent=None, mode_class=NormalMode, model=None):
        QOpenGLWidget.__init__(self, parent)
        self.setFocusPolicy(Qt.StrongFocus)

        # Visualization mode
        self.current_mode = mode_class(self)

        # Model
        self.model = model

        # Shader utility
        self.shader_program = QOpenGLShaderProgram(self)

        # VAO/VBO
        self.vao = QOpenGLVertexArrayObject()
        self.vbo = QOpenGLBuffer()

        # Camera/World/Projection
        self.camera = QMatrix4x4()
        self.world = QMatrix4x4()
        self.proj = QMatrix4x4()

        # Camera position
        self.xCamPos = 0.0
        self.yCamPos = 0.0
        self.zCamPos = -3.0

        # World rotation
        self.xRot = 0.0
        self.yRot = 0.0
        self.zRot = 0.0

        # Shader locations
        self.vertex_shader_source = 'View/Shaders/vertex.glsl'
        self.fragment_shader_source = 'View/Shaders/fragment.glsl'

        # MVP locations
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None
        self.test_value_loc = None

    def initializeGL(self):
        self.shader_program = QOpenGLShaderProgram(self.context())
        self.shader_program.addShaderFromSourceFile(QOpenGLShader.Vertex, self.vertex_shader_source)
        self.shader_program.addShaderFromSourceFile(QOpenGLShader.Fragment, self.fragment_shader_source)

        self.shader_program.bindAttributeLocation('a_position', _POSITION)
        self.shader_program.bindAttributeLocation('a_color', _COLOR)

        self.shader_program.link()
        self.shader_program.bind()

        # MVP locations
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')
        self.test_value_loc = self.shader_program.uniformLocation('test_value')

        # VAO/VBO
        # self.vao.create()
        # self.vao.bind()
        # self.vbo.create()
        # self.vbo.bind()

        # Vertex attributes setup
        # self.setup_vertex_attributes()

        # Camera setup
        self.camera.translate(self.xCamPos, self.yCamPos, self.zCamPos)

    def paintGL(self):
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

        self.world.setToIdentity()

        # Allow rotation of the world
        self.world.rotate(self.xRot / 16.0, 1, 0, 0)
        self.world.rotate(self.yRot / 16.0, 0, 1, 0)
        self.world.rotate(self.zRot / 16.0, 0, 0, 1)

        # Bind data of shaders to program
        # self.shader_program.link()
        self.shader_program.setUniformValue(self.proj_matrix_loc, self.proj)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, self.camera * self.world)
        # self.shader_program.bind()

        # Data
        position = np.array([-0.5, 0.5, 0.0,
                             -0.5, -0.5, 0.0,
                             0.5, -0.5, 0.0,
                             0.5, 0.5, 0.0], np.float32)

        color = np.array([1, 0, 0,
                          1, 0, 0,
                          0, 1, 0,
                          0, 1, 0], np.float32)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, position)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, color)

        # Draw data
        glDrawArrays(GL_QUADS, 0, 4)

    def resizeGL(self, w, h):
        # TODO Consider that we might need to change between perspective and orthogonal projection
        self.proj.setToIdentity()
        self.proj.perspective(45.0, (w / h), 0.01, 10000.0)

    # Controller dependent on current mode
    def mouseMoveEvent(self, event):
        self.current_mode.mouseMoveEvent(event)
        self.update()

    def mousePressEvent(self, event):
        self.current_mode.mousePressEvent(event)
        self.update()

    def wheelEvent(self, event):
        self.current_mode.wheelEvent(event)
        self.update()

    def setup_vertex_attributes(self):
        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, self.position)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, self.color)

        # self.vbo.release()

    @Slot()
    def update_mesh(self):
        # TODO On mesh load, delete current opengl vertices/faces, recreate them and update
        self.update()
