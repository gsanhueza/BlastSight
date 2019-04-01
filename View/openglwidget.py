#!/usr/bin/env python

import numpy as np

from OpenGL.GL import *
from PySide2.QtWidgets import QOpenGLWidget
from PySide2.QtGui import *
from PySide2.QtCore import Qt, Slot

from .normalmode import NormalMode

_POSITION = 0
_COLOR = 1


class OpenGLWidget(QOpenGLWidget):
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
        self.zCamPos = 0.0

        # World rotation
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        # Shader locations
        self.vertex_shader_source = 'View/Shaders/vertex.glsl'
        self.fragment_shader_source = 'View/Shaders/fragment.glsl'

        # MVP locations
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None

    def initializeGL(self):
        self.shader_program = QOpenGLShaderProgram(self.context())
        self.shader_program.addShaderFromSourceFile(QOpenGLShader.Vertex, self.vertex_shader_source)
        self.shader_program.addShaderFromSourceFile(QOpenGLShader.Fragment, self.fragment_shader_source)

        glBindAttribLocation(self.shader_program.programId(), _POSITION, 'a_position')
        glBindAttribLocation(self.shader_program.programId(), _COLOR, 'a_color')

        self.shader_program.link()
        self.shader_program.bind()

        # MVP locations
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')

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

        glViewport(0, 0, self.width(), self.height())

        # Bind data of shaders to program
        # self.shader_program.link()
        # self.shader_program.setUniformValue(self.proj_matrix_loc, self.proj)
        # self.shader_program.setUniformValue(self.model_view_matrix_loc, self.camera * self.world)
        # self.shader_program.bind()

        position = np.array([-0.5, 0.5, 0.0,
                             -0.5, -0.5, 0.0,
                             0.5, -0.5, 0.0,
                             0.5, 0.5, 0.0], np.float32)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, position)
        glEnableVertexAttribArray(_POSITION)

        color = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0], np.float32)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, color)
        glEnableVertexAttribArray(_COLOR)

        # Draw data
        glDrawArrays(GL_QUADS, 0, 4)

    def resizeGL(self, w, h):
        self.proj.setToIdentity()
        self.proj.perspective(45.0, (w / h), 0.01, 10000.0)

    # Controller dependent on current mode
    def mouseMoveEvent(self, event):
        self.current_mode.mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.current_mode.mousePressEvent(event)

    @Slot()
    def update_mesh(self):
        # TODO On mesh load, delete current opengl vertices/faces, recreate them and update
        self.update()
