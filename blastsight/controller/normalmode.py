#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt, QPoint
from .mode import Mode


class NormalMode(Mode):
    def __init__(self):
        super().__init__()
        self.name = 'Normal Mode'
        self.lastPos = None

    def mousePressEvent(self, event, widget):
        self.lastPos = QPoint(event.pos())

    def mouseDoubleClickEvent(self, event, widget):
        widget.detect_mesh_intersection(event.pos().x(), event.pos().y(), 1.0)

    def mouseMoveEvent(self, event, widget):
        if self.lastPos is None:
            return

        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        smoothness = max(widget.smoothness, 0.1)

        widget.world.setToIdentity()
        if event.buttons() == Qt.LeftButton:
            self.set_x_rotation(widget, widget.xCenterRot + dy / smoothness)
            self.set_z_rotation(widget, widget.zCenterRot + dx / smoothness)
        elif event.buttons() == Qt.RightButton:
            self.set_x_rotation(widget, widget.xCenterRot + dy / smoothness)
            self.set_y_rotation(widget, widget.yCenterRot + dx / smoothness)
        elif event.buttons() == Qt.MiddleButton:
            off_center = widget.off_center[2]
            distance_x = off_center / widget.width()
            distance_y = off_center / widget.height()
            self.set_x_movement(widget, widget.xCameraPos - (distance_x * dx))
            self.set_y_movement(widget, widget.yCameraPos + (distance_y * dy))

        self.lastPos = QPoint(event.pos())
