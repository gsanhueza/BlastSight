#!/usr/bin/env python


class Mode:
    def mousePressEvent(self, event, widget):
        pass

    def mouseMoveEvent(self, event, widget):
        pass

    def mouseReleaseEvent(self, event, widget):
        pass

    def wheelEvent(self, event, widget):
        dy = event.angleDelta().y()
        sign = dy / abs(dy) if abs(dy) > 1e-6 else 0.0

        rate = 0.1
        movement_rate = rate / (1.0 + max(0.0, min(sign, rate)))

        off_center = max(widget.zCameraPos - widget.zCentroidPos, 0.0)
        shift = -sign * movement_rate * max(-sign, off_center)

        self.set_z_movement(widget, widget.zCameraPos + shift)

    def overpaint(self, widget):
        pass

    @staticmethod
    def normalize_angle(angle):
        return angle % 360

    @staticmethod
    def set_x_rotation(widget, angle):
        angle = Mode.normalize_angle(angle)
        if angle != widget.xCentroidRot:
            widget.xCentroidRot = angle

    @staticmethod
    def set_y_rotation(widget, angle):
        angle = Mode.normalize_angle(angle)
        if angle != widget.yCentroidRot:
            widget.yCentroidRot = angle

    @staticmethod
    def set_z_rotation(widget, angle):
        angle = Mode.normalize_angle(angle)
        if angle != widget.zCentroidRot:
            widget.zCentroidRot = angle

    @staticmethod
    def set_x_movement(widget, position):
        if abs(position - widget.xCameraPos) > 1e-6:
            widget.xCameraPos = position

    @staticmethod
    def set_y_movement(widget, position):
        if abs(position - widget.yCameraPos) > 1e-6:
            widget.yCameraPos = position

    @staticmethod
    def set_z_movement(widget, position):
        if abs(position - widget.zCameraPos) > 1e-6:
            widget.zCameraPos = position
