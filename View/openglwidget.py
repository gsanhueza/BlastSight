#!/usr/bin/env python

import numpy as np
from OpenGL import GL, GLUT
from PySide2.QtWidgets import QOpenGLWidget
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter

from .normalmode import NormalMode


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None, mode_class=NormalMode):
        print("Init: OpenGLWidget")
        QOpenGLWidget.__init__(self, parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.currentMode = mode_class(self)

        self.rotation = 0

    def initializeGL(self):
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

    # Controller dependent on current mode
    def mouseMoveEvent(self, event):
        self.currentMode.mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.currentMode.mousePressEvent(event)
