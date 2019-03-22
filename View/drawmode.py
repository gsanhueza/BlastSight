#!/usr/bin/env python

from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import *
from OpenGL import GL


class DrawMode():
    def __init__(self, widget):
        self.openglwidget = widget
        self.openglwidget.parent().setWindowTitle("Draw Mode")
        print("MODE: Draw Mode")

    def mouseMoveEvent(self, event):
        print("Unable to move in Draw Mode")
        self.openglwidget.rotation = 0
        self.openglwidget.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print("Pressing in Draw Mode with LeftButton")
        elif event.button() == Qt.MouseButton.MiddleButton:
            print("Pressing in Draw Mode with MiddleButton")
        elif event.button() == Qt.MouseButton.RightButton:
            print("Pressing in Draw Mode with RightButton")

        self.openglwidget.update()
