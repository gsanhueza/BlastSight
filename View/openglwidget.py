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
        self.position_vbo = QOpenGLBuffer()
        self.color_vbo = QOpenGLBuffer()
        self.indices_ibo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)

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

        # Data
        self.position = None
        self.color = None
        self.indices = None

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

        # Data
        self.position = np.array([-0.5, 0.5, 0.0,
                                  -0.5, -0.5, 0.0,
                                  0.5, 0.5, 0.0], np.float32)

        self.color = np.array([1.0, 0.0, 0.0,
                               0.0, 1.0, 0.0,
                               0.0, 0.0, 1.0], np.float32)

        self.indices = np.array([0, 1, 2,
                                 3, 4, 5,
                                 6, 7, 8], np.int)

        # VAO/VBO/IBO creation
        self.vao.create()
        self.position_vbo.create()
        self.color_vbo.create()
        self.indices_ibo.create()

        self.vao.bind()

        # Setup vertex attributes
        self.setup_vertex_attribs()

        # Camera setup
        self.camera.translate(self.xCamPos, self.yCamPos, self.zCamPos)

    def setup_vertex_attribs(self):
        _SIZE_OF_GL_FLOAT = 4

        self.position_vbo.bind()
        glEnableVertexAttribArray(_POSITION)
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.position.size, self.position, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        self.color_vbo.bind()
        glEnableVertexAttribArray(_COLOR)
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.color.size, self.color, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        self.indices_ibo.bind()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)  # FIXME Fails here

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
        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, self.proj)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, self.camera * self.world)

        # Draw data
        # glDrawArrays(GL_TRIANGLES, 0, self.position.size)
        glDrawElements(GL_TRIANGLES, self.indices.size, GL_UNSIGNED_INT, 0)

        self.shader_program.release()

    def resizeGL(self, w, h):
        # TODO Consider that we might need to change between perspective and orthogonal projection... in the controller (mode)
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

    @Slot()
    def update_mesh(self):
        # TODO On mesh load, delete current opengl vertices/faces, recreate them and update
        import random

        # This works! But we need to update drawArrays to GL_TRIANGLES
        # self.position = np.array(self.model.get_vertices(), np.float32)
        self.position = np.array([-0.5, 0.5, 0.0,
                                  -0.5, -0.5, 0.0,
                                  0.5, 0.5, 0.0,
                                  -0.3, -0.5, 0.0,
                                  0.7, -0.5, 0.0,
                                  0.7, 0.5, 0.0], np.float32)
        self.color = np.array([random.random() for _ in range(self.position.size)], np.float32)

        self.setup_vertex_attribs()

        self.update()
