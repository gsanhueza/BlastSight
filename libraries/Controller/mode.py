#!/usr/bin/env python


class Mode:
    def __init__(self, widget):
        self.widget = widget
        self.widget.update()

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def wheelEvent(self, event):
        pass

    def overpaint(self):
        pass

    def normalize_angle(self, angle):
        return angle % 360

    def set_x_rotation(self, angle):
        angle = self.normalize_angle(angle)
        if angle != self.widget.xWorldRot:
            self.widget.xWorldRot = angle

    def set_y_rotation(self, angle):
        angle = self.normalize_angle(angle)
        if angle != self.widget.yWorldRot:
            self.widget.yWorldRot = angle

    def set_z_rotation(self, angle):
        angle = self.normalize_angle(angle)
        if angle != self.widget.zWorldRot:
            self.widget.zWorldRot = angle

    def set_x_movement(self, position):
        if abs(position - self.widget.xWorldPos) > 0.01:
            self.widget.xWorldPos = position

    def set_y_movement(self, position):
        if abs(position - self.widget.yWorldPos) > 0.01:
            self.widget.yWorldPos = position
