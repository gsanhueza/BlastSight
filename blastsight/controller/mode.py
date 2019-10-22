#!/usr/bin/env python


#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

class Mode:
    def __init__(self):
        self.name = 'Base mode'

    def mousePressEvent(self, event, widget):
        pass

    def mouseMoveEvent(self, event, widget):
        pass

    def mouseReleaseEvent(self, event, widget):
        pass

    def mouseDoubleClickEvent(self, event, widget):
        pass

    def wheelEvent(self, event, widget):
        dy = event.angleDelta().y()
        sign = dy / abs(dy) if abs(dy) > 1e-12 else 0.0
        smoothness = max(widget.smoothness, 0.1)

        # Arbitrary number, but dependent on viewer's smoothness
        rate = 0.4 / smoothness
        movement_rate = rate / (1.0 + max(0.0, min(sign, rate)))

        off_center = widget.off_center[2]
        shift = -sign * movement_rate * max(-sign, off_center) / smoothness

        self.set_z_movement(widget, widget.zCameraPos + shift)

    @staticmethod
    def set_x_rotation(widget, angle: float) -> None:
        widget.xCenterRot = angle % 360

    @staticmethod
    def set_y_rotation(widget, angle: float) -> None:
        widget.yCenterRot = angle % 360

    @staticmethod
    def set_z_rotation(widget, angle: float) -> None:
        widget.zCenterRot = angle % 360

    @staticmethod
    def set_x_movement(widget, position: float) -> None:
        widget.xCameraPos = position

    @staticmethod
    def set_y_movement(widget, position: float) -> None:
        widget.yCameraPos = position

    @staticmethod
    def set_z_movement(widget, position: float) -> None:
        widget.zCameraPos = position
