#!/usr/bin/env python

from PySide2.QtCore import Qt
from Controller.mode import Mode


class DrawMode(Mode):
    def __init__(self, widget):
        super().__init__(widget)
        self.widget.parent().setWindowTitle("Draw Mode")
        print("MODE: Draw Mode")

    def mouseMoveEvent(self, event):
        print("Unable to move in Draw Mode")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print("Pressing in Draw Mode with LeftButton")
        elif event.button() == Qt.MouseButton.MiddleButton:
            print("Pressing in Draw Mode with MiddleButton")
        elif event.button() == Qt.MouseButton.RightButton:
            print("Pressing in Draw Mode with RightButton")

        print(f'Pos: {event.pos()}, widget.painter: {self.widget.painter}')
