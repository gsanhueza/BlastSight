#!/usr/bin/env python

from PyQt5.QtCore import Qt, QPoint
from Controller.mode import Mode


"""
General methods
"""


def normalize_angle(angle):
    while angle < 0:
        angle += 360 * 16
    while angle > 360 * 16:
        angle -= 360 * 16
    return angle


class NormalMode(Mode):
    def __init__(self, widget):
        super().__init__(widget)
        print("MODE: Normal Mode")

        self.lastPos = None

    def mousePressEvent(self, event):
        self.lastPos = QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        self.widget.world.setToIdentity()
        if event.buttons() == Qt.LeftButton:
            self.set_x_rotation(self.widget.xWorldRot + 8 * dy)
            self.set_y_rotation(self.widget.yWorldRot + 8 * dx)
        elif event.buttons() == Qt.MiddleButton:
            self.set_x_movement(self.widget.xWorldPos + (dx / 200.0))
            self.set_y_movement(self.widget.yWorldPos - (dy / 200.0))
        elif event.buttons() == Qt.RightButton:
            self.set_x_rotation(self.widget.xWorldRot + 8 * dy)
            self.set_z_rotation(self.widget.zWorldRot - 8 * dx)

        self.lastPos = QPoint(event.pos())

    def wheelEvent(self, event):
        self.widget.zWorldPos += (event.angleDelta().y() / 120)

    def set_x_rotation(self, angle):
        angle = normalize_angle(angle)
        if angle != self.widget.xWorldRot:
            self.widget.xWorldRot = angle

    def set_y_rotation(self, angle):
        angle = normalize_angle(angle)
        if angle != self.widget.yWorldRot:
            self.widget.yWorldRot = angle

    def set_z_rotation(self, angle):
        angle = normalize_angle(angle)
        if angle != self.widget.zWorldRot:
            self.widget.zWorldRot = angle

    def set_x_movement(self, position):
        if abs(position - self.widget.xWorldPos) > 0.01:
            self.widget.xWorldPos = position

    def set_y_movement(self, position):
        if abs(position - self.widget.yWorldPos) > 0.01:
            self.widget.yWorldPos = position
