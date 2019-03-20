#!/usr/bin/env python

from PySide2.QtCore import Slot, Qt
from PySide2.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from normalmode import NormalMode


class OGLWidget(QGLWidget):
    def __init__(self, parent=None, mode_class=NormalMode):
        QGLWidget.__init__(self, parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.currentMode = mode_class(self)

    def initializeGL(self):
         glClearColor(0.0, 0.0, 0.0, 1.0)

    def mouseMoveEvent(self, event):
        self.currentMode.mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.currentMode.mousePressEvent(event)

    def paintGL(self):
        self.currentMode.paintGL()
