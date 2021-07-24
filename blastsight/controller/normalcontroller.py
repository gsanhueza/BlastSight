#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt, QPoint
from qtpy.QtGui import QMouseEvent
from .basecontroller import BaseController


class NormalController(BaseController):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.name = 'Normal'
        self.lastPos = None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        self.lastPos = QPoint(event.pos())

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        x, y, z = [event.pos().x(), event.pos().y(), 1]
        origin = self.viewer.origin_from_click(x, y, z)
        ray = self.viewer.ray_from_click(x, y, z)

        self.viewer.intersect_elements(origin, ray)

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
