#!/usr/bin/env python

import numpy as np

from OpenGL import GL, GLUT
from PySide2.QtWidgets import QOpenGLWidget
from PySide2.QtGui import *
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPainter

from .normalmode import NormalMode


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None, mode_class=NormalMode, model=None):
        QOpenGLWidget.__init__(self, parent)
        self.setFocusPolicy(Qt.StrongFocus)

        # Visualization mode
        self.current_mode = mode_class(self)

        # Model
        self.model = model

        # Shader utility
        self.program = QOpenGLShaderProgram(self)
        self.rotation = 0

        # VAO
        self.vao = QOpenGLVertexArrayObject()

        # Camera
        self.camera = QMatrix4x4()
        self.xCamPos = 0.0
        self.yCamPos = 0.0
        self.zCamPos = 0.0

    def initializeGL(self):
        # FIXME Are you sure you'll use just one shader for everything?
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, 'View/Shaders/vertex.glsl')
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, 'View/Shaders/fragment.glsl')

        self.program.bindAttributeLocation('vertex', 0)
        self.program.bindAttributeLocation('color', 1)
        self.program.link()

        self.program.bind()

        self.modelViewMatrixLoc = self.program.uniformLocation('modelViewMatrix')
        self.projMatrixLoc = self.program.uniformLocation('projMatrix')

        self.vao.create()

        # Our camera has an initial position.
        self.camera.setToIdentity()
        self.camera.translate(self.xCamPos, self.yCamPos, self.zCamPos);

        self.program.release()

        ## TODO Delete this scheiße below

        print(self.model.get_vertices())
        vertices = np.array([0.0, 1.0, -1.0, -1.0, 1.0, -1.0], dtype=np.float32)

        bufferId = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, bufferId)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

    def paintGL(self):
        painter = QPainter(self)

        GL.glRotated(self.rotation, 0.0, 1.0, 0.0)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    def resizeGL(self, width, height):
        super().resizeGL(width, height)

    # Controller dependent on current mode
    def mouseMoveEvent(self, event):
        self.current_mode.mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.current_mode.mousePressEvent(event)

    @Slot()
    def update_mesh():
        # TODO On mesh load, delete current opengl vertices/faces, recreate them and update
        self.update()
