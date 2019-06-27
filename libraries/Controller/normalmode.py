#!/usr/bin/env python

from qtpy.QtCore import Qt, QPoint
from .mode import Mode


class NormalMode(Mode):
    def __init__(self, widget):
        super().__init__(widget)
        print("MODE: Normal Mode")
        self.lastPos = None

    def mousePressEvent(self, event):
        self.lastPos = QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        self.widget.world.setToIdentity()
        if event.buttons() == Qt.LeftButton:
            self.set_x_rotation(self.widget.xWorldRot + dy)
            self.set_y_rotation(self.widget.yWorldRot + dx)
        elif event.buttons() == Qt.MiddleButton:
            # FIXME Dependent on aspect ratio
            distance_x = 200 * abs(self.widget.zWorldPos + self.widget.centroid[2]) / self.widget.width()
            distance_y = 200 * abs(self.widget.zWorldPos + self.widget.centroid[2]) / self.widget.height()
            self.set_x_movement(self.widget.xWorldPos + (distance_x * dx / 200.0))
            self.set_y_movement(self.widget.yWorldPos - (distance_y * dy / 200.0))
        elif event.buttons() == Qt.RightButton:
            self.set_x_rotation(self.widget.xWorldRot + dy)
            self.set_z_rotation(self.widget.zWorldRot - dx)

        self.lastPos = QPoint(event.pos())

    def wheelEvent(self, event):
        # self.widget.zWorldPos += (event.angleDelta().y() / 120)
        self.widget.zWorldPos *= pow(1.2, -event.angleDelta().y() / 120)
