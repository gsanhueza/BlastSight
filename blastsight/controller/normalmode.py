#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt, QPoint
from qtpy.QtGui import QMouseEvent
from .mode import Mode


class NormalMode(Mode):
    def __init__(self):
        super().__init__()
        self.name = 'Normal Mode'
        self.lastPos = None

    def mousePressEvent(self, event: QMouseEvent, viewer) -> None:
        self.lastPos = QPoint(event.pos())

    def mouseDoubleClickEvent(self, event: QMouseEvent, viewer) -> None:
        viewer.detect_mesh_intersection(event.pos().x(), event.pos().y(), 1.0)

    def mouseMoveEvent(self, event: QMouseEvent, viewer) -> None:
        if self.lastPos is None:
            return

        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        smoothness = max(viewer.smoothness, 0.1)

        viewer.world.setToIdentity()
        if event.buttons() == Qt.LeftButton:
            self.set_x_rotation(viewer, viewer.xCenterRot + dy / smoothness)
            self.set_z_rotation(viewer, viewer.zCenterRot + dx / smoothness)
        elif event.buttons() == Qt.RightButton:
            self.set_x_rotation(viewer, viewer.xCenterRot + dy / smoothness)
            self.set_y_rotation(viewer, viewer.yCenterRot + dx / smoothness)
        elif event.buttons() == Qt.MiddleButton:
            off_center = viewer.off_center[2]
            distance_x = off_center / viewer.width()
            distance_y = off_center / viewer.height()
            self.set_x_movement(viewer, viewer.xCameraPos - (distance_x * dx))
            self.set_y_movement(viewer, viewer.yCameraPos + (distance_y * dy))

        self.lastPos = QPoint(event.pos())
