#!/usr/bin/env python

from PyQt5.QtCore import QPoint
from Controller.mode import Mode


class FreeMode(Mode):
    def __init__(self, widget):
        super().__init__(widget)
        print("MODE: Free Mode")

        self.lastPos = None

    def mousePressEvent(self, event):
        self.lastPos = QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        self.set_x_movement(self.widget.xWorldPos + (dx / 200.0))
        self.set_y_movement(self.widget.yWorldPos - (dy / 200.0))

        self.lastPos = QPoint(event.pos())

    def wheelEvent(self, event):
        self.widget.zWorldPos += (event.angleDelta().y() / 120)

    def set_x_movement(self, position):
        if abs(position - self.widget.xWorldPos) > 0.01:
            self.widget.xWorldPos = position

    def set_y_movement(self, position):
        if abs(position - self.widget.yWorldPos) > 0.01:
            self.widget.yWorldPos = position
