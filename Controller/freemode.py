#!/usr/bin/env python

from PySide2.QtCore import QPoint
from Controller.mode import Mode


class FreeMode(Mode):
    def __init__(self, widget):
        super().__init__(self)
        self.widget = widget
        self.widget.parent().setWindowTitle("Free Mode")
        self.lastPos = None
        print("MODE: Free Mode")

    def mousePressEvent(self, event):
        self.lastPos = QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        self.set_x_movement(self.widget.xCamPos + (dx / 200.0))
        self.set_y_movement(self.widget.yCamPos - (dy / 200.0))

        self.lastPos = QPoint(event.pos())

    def set_x_movement(self, position):
        if abs(position - self.widget.xCamPos) > 0.01:
            self.widget.xCamPos = position
        self.widget.camera.setToIdentity()
        self.widget.camera.translate(self.widget.xCamPos,
                                     self.widget.yCamPos,
                                     self.widget.zCamPos)

    def set_y_movement(self, position):
        if abs(position - self.widget.yCamPos) > 0.01:
            self.widget.yCamPos = position
        self.widget.camera.setToIdentity()
        self.widget.camera.translate(self.widget.xCamPos,
                                     self.widget.yCamPos,
                                     self.widget.zCamPos)
