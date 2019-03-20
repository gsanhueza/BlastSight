#!/usr/bin/env python

from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class DrawMode():
    def __init__(self, widget):
        self.openglwidget = widget
        self.openglwidget.parent().setWindowTitle("Draw Mode")
        print("MODE: Draw Mode")

    def paintGL(self):
        painter = QPainter(self.openglwidget)

        painter.begin(self.openglwidget)
        glClearColor(0.8, 0.5, 7, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBegin(GL_LINES)
        glColor3f(1.0,1.0,1.0)
        glVertex2f(0,0)
        glVertex2f(200,200)
        glEnd()

        painter.drawText(50, 50, "Draw Mode")
        painter.end()

    def mouseMoveEvent(self, event):
        print("Unable to move in Draw Mode")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print("Pressing in Draw Mode with LeftButton")
            glClearColor(0.0, 0.0, 0.0, 1.0)
        elif event.button() == Qt.MouseButton.MiddleButton:
            print("Pressing in Draw Mode with MiddleButton")
        elif event.button() == Qt.MouseButton.RightButton:
            print("Pressing in Draw Mode with RightButton")
            glClearColor(0.0, 0.0, 0.0, 1.0)

        self.openglwidget.update()

