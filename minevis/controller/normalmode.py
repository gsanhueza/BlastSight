#!/usr/bin/env python

from qtpy.QtCore import Qt, QPoint
from .mode import Mode


class NormalMode(Mode):
    def __init__(self):
        print("MODE: Normal Mode")
        self.lastPos = None

    def mousePressEvent(self, event, widget):
        self.lastPos = QPoint(event.pos())

    def mouseMoveEvent(self, event, widget):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        widget.world.setToIdentity()
        if event.buttons() == Qt.LeftButton:
            self.set_x_rotation(widget, widget.xCenterRot + dy)
            self.set_z_rotation(widget, widget.zCenterRot + dx)
        elif event.buttons() == Qt.RightButton:
            self.set_x_rotation(widget, widget.xCenterRot + dy)
            self.set_y_rotation(widget, widget.yCenterRot + dx)
        elif event.buttons() == Qt.MiddleButton:
            distance_x = abs(widget.zCameraPos + widget.zCenterPos) / widget.width()
            distance_y = abs(widget.zCameraPos + widget.zCenterPos) / widget.height()
            self.set_x_movement(widget, widget.xCameraPos - (distance_x * dx))
            self.set_y_movement(widget, widget.yCameraPos + (distance_y * dy))

        self.lastPos = QPoint(event.pos())
