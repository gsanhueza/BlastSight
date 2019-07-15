#!/usr/bin/env python


class Mode:
    def mousePressEvent(self, event, widget):
        pass

    def mouseMoveEvent(self, event, widget):
        pass

    def mouseReleaseEvent(self, event, widget):
        pass

    def wheelEvent(self, event, widget):
        pass

    def overpaint(self, widget):
        pass

    @staticmethod
    def normalize_angle(angle):
        return angle % 360

    @staticmethod
    def set_x_rotation(widget, angle):
        angle = Mode.normalize_angle(angle)
        if angle != widget.xWorldRot:
            widget.xWorldRot = angle

    @staticmethod
    def set_y_rotation(widget, angle):
        angle = Mode.normalize_angle(angle)
        if angle != widget.yWorldRot:
            widget.yWorldRot = angle

    @staticmethod
    def set_z_rotation(widget, angle):
        angle = Mode.normalize_angle(angle)
        if angle != widget.zWorldRot:
            widget.zWorldRot = angle

    @staticmethod
    def set_x_movement(widget, position):
        if abs(position - widget.xCameraPos) > 0.01:
            widget.xCameraPos = position

    @staticmethod
    def set_y_movement(widget, position):
        if abs(position - widget.yCameraPos) > 0.01:
            widget.yCameraPos = position
