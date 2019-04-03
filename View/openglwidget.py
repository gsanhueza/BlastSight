#!/usr/bin/env python

import numpy as np

from OpenGL.GL import *
from PySide2.QtWidgets import QOpenGLWidget
from PySide2.QtGui import QOpenGLShaderProgram
from PySide2.QtGui import QOpenGLShader
from PySide2.QtGui import QOpenGLBuffer
from PySide2.QtGui import QOpenGLVertexArrayObject
from PySide2.QtGui import QMatrix4x4
from PySide2.QtCore import Qt
from PySide2.QtCore import Slot

from Controller.normalmode import NormalMode

_POSITION = 0
_COLOR = 1


class OpenGLWidget(QOpenGLWidget):
    # FIXME We might not get a model every time.
    # FIXME We need to have a fallback option to only receive vertices, for example
    def __init__(self, parent=None, mode_class=NormalMode, model=None):
        QOpenGLWidget.__init__(self, parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        # Controller mode
        self.current_mode = mode_class(self)

        # Model
        self.model = model

        # Shaders
        self.shader_program = QOpenGLShaderProgram(self)
        self.vertex_shader = None
        self.fragment_shader = None
        self.geometry_shader = None

        # VAO/VBO
        self.vao = QOpenGLVertexArrayObject()
        self.position_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.color_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
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
        self.geometry_shader_source = 'View/Shaders/geometry.glsl'

        # MVP locations
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None
        self.test_value_loc = None

        # Data
        self.position = None
        self.color = None
        self.indices = None

        # Wireframe (Shader toggling)
        self.wireframe_enabled = True

    def initializeGL(self):
        self.shader_program = QOpenGLShaderProgram(self.context())

        # Create shaders
        self.vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        self.fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        self.geometry_shader = QOpenGLShader(QOpenGLShader.Geometry)

        # Compile shaders
        self.vertex_shader.compileSourceFile(self.vertex_shader_source)
        self.fragment_shader.compileSourceFile(self.fragment_shader_source)
        self.geometry_shader.compileSourceFile(self.geometry_shader_source)

        # Add shaders to program
        self.shader_program.addShader(self.vertex_shader)
        self.shader_program.addShader(self.fragment_shader)
        self.shader_program.addShader(self.geometry_shader)

        # Bind attribute locations
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

        self.indices = np.array([0, 1, 2], np.uint32)  # Finally! This wasn't np.int, but np.uint32

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

        self.vao.bind()

        self.position_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.position.size, self.position, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        self.color_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.color.size, self.color, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        self.indices_ibo.bind()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        self.vao.release()

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
        self.vao.bind()
        # glDrawArrays(GL_TRIANGLES, 0, self.position.size)
        self.indices_ibo.bind()
        glDrawElements(GL_TRIANGLES, self.indices.size, GL_UNSIGNED_INT, None)
        self.vao.release()

        self.shader_program.release()

    def resizeGL(self, w, h):
        # FIXME We might need to change between perspective and orthogonal projection... in the controller (mode)
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
        # TODO Set a decent color, not a random one
        import random

        self.position = np.array(self.model.get_vertices(), np.float32)
        self.indices = np.array(self.model.get_indices(), np.uint32)
        self.color = np.array([random.random() for _ in range(self.position.size)], np.float32)

        self.setup_vertex_attribs()
        self.update()

    @Slot()
    def toggle_wireframe(self):
        if self.wireframe_enabled:
            self.shader_program.removeShader(self.geometry_shader)
            self.wireframe_enabled = False
        else:
            self.shader_program.addShader(self.geometry_shader)
            self.wireframe_enabled = True

        self.update()

    # FIXME Should we (openglwidget) or mainwindow handle this? Should we notify mainwindow of an error?
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.model.load_mesh(file_path)
        self.update_mesh()

        # Check if we're part of a MainWindow or a standalone widget
        if self.parent():
            self.parent().statusBar.showMessage('Drop')
