#!/usr/bin/env python

from PySide2.QtCore import Qt
from Controller.mode import Mode


class DrawMode(Mode):
    def __init__(self, widget):
        super().__init__(widget)
        self.widget.parent().setWindowTitle("Draw Mode")
        print("MODE: Draw Mode")

        self.active = False
        self.lastPos = None

    def mouseMoveEvent(self, event):
        print("Unable to move in Draw Mode")
        self.lastPos = event.pos()

    def mousePressEvent(self, event):
        self.active = True
        self.lastPos = event.pos()

        if event.button() == Qt.MouseButton.LeftButton:
            print("Pressing in Draw Mode with LeftButton")
        elif event.button() == Qt.MouseButton.MiddleButton:
            print("Pressing in Draw Mode with MiddleButton")
        elif event.button() == Qt.MouseButton.RightButton:
            print("Pressing in Draw Mode with RightButton")

    def mouseReleaseEvent(self, event):
        self.lastPos = event.pos()
        self.active = False

    def modify_paintgl(self):
        if self.active or True:
            self.widget.painter.begin(self.widget)
            self.widget.painter.setPen(Qt.yellow)
            self.widget.painter.drawText(200, 50, f'Draw enabled = {self.active}')
            self.widget.painter.drawText(200, 80, f'event.pos()  = {self.lastPos}')
            self.widget.painter.end()
