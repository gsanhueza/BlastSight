#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QMouseEvent, QWheelEvent, QKeyEvent


class BaseController:
    def __init__(self, viewer):
        self.name = 'Base'
        self.viewer = viewer

    def mousePressEvent(self, event: QMouseEvent) -> None:
        x, y, z = [event.pos().x(), event.pos().y(), 0]
        origin = self.viewer.origin_from_click(x, y, z)
        ray = self.viewer.ray_from_click(x, y, z)

        self.viewer.signal_screen_clicked.emit([x, y, z])
        self.viewer.signal_ray_generated.emit({'origin': origin, 'ray': ray})

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pass

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pass

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        pass

    def keyPressEvent(self, event: QKeyEvent) -> None:
        pass

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        pass

    def wheelEvent(self, event: QWheelEvent) -> None:
        dy = event.angleDelta().y()
        sign = dy / abs(dy) if abs(dy) > 1e-12 else 0.0
        smoothness = max(self.viewer.smoothness, 0.1)

        # Arbitrary number, but dependent on viewer's smoothness
        rate = 0.4 / smoothness
        movement_rate = rate / (1.0 + max(0.0, min(sign, rate)))

        off_center = self.viewer.off_center[2]
        shift = -sign * movement_rate * max(-sign, off_center) / smoothness

        self.viewer.translate(x=0, y=0, z=shift)
