#!/usr/bin/env python

from PySide2.QtCore import Qt, QPoint
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
        self.widget.parent().setWindowTitle("Normal Mode")
        self.lastPos = None
        print("MODE: Normal Mode")

    def mousePressEvent(self, event):
        self.lastPos = QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() == Qt.LeftButton:
            self.set_x_rotation(self.widget.xRot + 8 * dy)
            self.set_y_rotation(self.widget.yRot + 8 * dx)
        elif event.buttons() == Qt.RightButton:
            self.set_x_rotation(self.widget.xRot + 8 * dy)
            self.set_z_rotation(self.widget.zRot - 8 * dx)

        self.lastPos = QPoint(event.pos())

    def wheelEvent(self, event):
        self.widget.zCamPos += (event.delta() / 120)
        self.widget.camera.setToIdentity()
        self.widget.camera.translate(self.widget.xCamPos,
                                     self.widget.yCamPos,
                                     self.widget.zCamPos)

    def set_x_rotation(self, angle):
        angle = normalize_angle(angle)
        if angle != self.widget.xRot:
            self.widget.xRot = angle

    def set_y_rotation(self, angle):
        angle = normalize_angle(angle)
        if angle != self.widget.yRot:
            self.widget.yRot = angle

    def set_z_rotation(self, angle):
        angle = normalize_angle(angle)
        if angle != self.widget.zRot:
            self.widget.zRot = angle
