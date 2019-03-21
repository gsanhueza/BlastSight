#!/usr/bin/env python

from PySide2.QtCore import Qt
from PySide2.QtGui import *
from OpenGL import GL


class NormalMode():
    def __init__(self, widget):
        self.openglwidget = widget
        self.openglwidget.parent().setWindowTitle("Normal Mode")
        print("MODE: Normal Mode")

    def mouseMoveEvent(self, event):
        print("Moving in Normal Mode")
        self.openglwidget.rotation += 0.1
        self.openglwidget.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print("Pressing in Normal Mode with LeftButton")
        elif event.button() == Qt.MouseButton.MiddleButton:
            print("Pressing in Normal Mode with MiddleButton")
        elif event.button() == Qt.MouseButton.RightButton:
            print("Pressing in Normal Mode with RightButton")

        self.openglwidget.update()
