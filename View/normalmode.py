#!/usr/bin/env python

from PySide2.QtCore import Qt, QPoint


class NormalMode:
    def __init__(self, widget):
        self.widget = widget
        self.widget.parent().setWindowTitle("Normal Mode")
        print("MODE: Normal Mode")

    def mousePressEvent(self, event):
        self.lastPos = QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() == Qt.LeftButton:
            self.setXRotation(self.widget.xRot + 8 * dy)
            self.setYRotation(self.widget.yRot + 8 * dx)
        elif event.buttons() == Qt.RightButton:
            self.setXRotation(self.widget.xRot + 8 * dy)
            self.setZRotation(self.widget.zRot + 8 * dx)

        self.lastPos = QPoint(event.pos())

    def wheelEvent(self, event):
        self.widget.zCamPos += (event.delta() / 1200)
        self.widget.camera.setToIdentity()
        self.widget.camera.translate(self.widget.xCamPos,
                                     self.widget.yCamPos,
                                     self.widget.zCamPos)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.widget.xRot:
            self.widget.xRot = angle

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.widget.yRot:
            self.widget.yRot = angle

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.widget.zRot:
            self.widget.zRot = angle

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle
