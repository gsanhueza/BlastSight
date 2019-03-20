#!/usr/bin/env python

from PySide2.QtCore import Qt
from PySide2.QtGui import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class NormalMode():
    def __init__(self, widget):
        self.openglwidget = widget
        self.openglwidget.parent().setWindowTitle("Normal Mode")
        print("MODE: Normal Mode")

    def paintGL(self):
        painter = QPainter(self.openglwidget)

        painter.begin(self.openglwidget)
        glClearColor(0.2, 0.5, 7, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBegin(GL_LINES)
        glColor3f(1.0,1.0,1.0)
        glVertex2f(0,0)
        glVertex2f(200,200)
        glEnd()

        painter.drawText(100, 50, "Normal Mode")
        painter.end()

    def mouseMoveEvent(self, event):
        print("Moving in Normal Mode")
        glTranslatef((event.x() - 400)/5000.0, 0, 0)
        self.openglwidget.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print("Pressing in Normal Mode with LeftButton")
            glClearColor(0.0, 0.0, 0.0, 1.0)
        elif event.button() == Qt.MouseButton.MiddleButton:
            print("Pressing in Normal Mode with MiddleButton")
        elif event.button() == Qt.MouseButton.RightButton:
            print("Pressing in Normal Mode with RightButton")
            glClearColor(0.0, 0.0, 0.0, 1.0)

        self.openglwidget.update()
