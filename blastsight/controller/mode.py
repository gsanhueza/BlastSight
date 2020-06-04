#!/usr/bin/env python


#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QMouseEvent, QWheelEvent


class Mode:
    def __init__(self, viewer):
        self.name = 'Base mode'
        self.viewer = viewer

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pass

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pass

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pass

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
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
