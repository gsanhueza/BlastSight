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
            self.set_x_rotation(widget, widget.xWorldRot + dy)
            self.set_y_rotation(widget, widget.yWorldRot + dx)
        elif event.buttons() == Qt.MiddleButton:
            # FIXME Dependent on aspect ratio
            distance_x = 200 * abs(widget.zCameraPos + widget.centroid[2]) / widget.width()
            distance_y = 200 * abs(widget.zCameraPos + widget.centroid[2]) / widget.height()
            self.set_x_movement(widget, widget.xCameraPos + (distance_x * dx / 200.0))
            self.set_y_movement(widget, widget.yCameraPos - (distance_y * dy / 200.0))
        elif event.buttons() == Qt.RightButton:
            self.set_x_rotation(widget, widget.xWorldRot + dy)
            self.set_z_rotation(widget, widget.zWorldRot - dx)

        self.lastPos = QPoint(event.pos())

    def wheelEvent(self, event, widget):
        # self.widget.zWorldPos += (event.angleDelta().y() / 120)
        widget.zCameraPos *= pow(1.2, -event.angleDelta().y() / 120)
