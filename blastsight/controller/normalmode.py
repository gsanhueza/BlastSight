#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt, QPoint
from qtpy.QtGui import QMouseEvent
from .mode import Mode


class NormalMode(Mode):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.name = 'Normal Mode'
        self.lastPos = None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.lastPos = QPoint(event.pos())

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.viewer.detect_mesh_intersection(event.pos().x(), event.pos().y(), 1.0)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.lastPos is None:
            return

        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        smoothness = max(self.viewer.smoothness, 0.1)

        # viewer.world.setToIdentity()
        if event.buttons() == Qt.LeftButton:
            self.viewer.rotate(alpha=dy / smoothness, beta=0, gamma=dx / smoothness)

        elif event.buttons() == Qt.RightButton:
            self.viewer.rotate(alpha=dy / smoothness, beta=dx / smoothness, gamma=0)

        elif event.buttons() == Qt.MiddleButton:
            off_center = self.viewer.off_center[2]
            distance_x = off_center / self.viewer.width()
            distance_y = off_center / self.viewer.height()

            self.viewer.translate(x=-distance_x * dx, y=distance_y * dy, z=0)

        self.lastPos = QPoint(event.pos())
