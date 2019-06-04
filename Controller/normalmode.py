#!/usr/bin/env python

from PyQt5.QtCore import Qt, QPoint
from Controller.mode import Mode


class NormalMode(Mode):
    def __init__(self, widget):
        super().__init__(widget)
        print("MODE: Normal Mode")

        self.lastPos = None

    def mousePressEvent(self, event):
        self.lastPos = QPoint(event.pos())

    def mouseReleaseEvent(self, event):
        intersection = self.widget.detect_intersection(event.pos().x(), event.pos().y(), 1.0)

        print(f'Intersection at {intersection}')
        print('-------------------------------')

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        self.widget.world.setToIdentity()
        if event.buttons() == Qt.LeftButton:
            self.set_x_rotation(self.widget.xWorldRot + dy)
            self.set_y_rotation(self.widget.yWorldRot + dx)
        elif event.buttons() == Qt.MiddleButton:
            self.set_x_movement(self.widget.xWorldPos + (dx / 200.0))
            self.set_y_movement(self.widget.yWorldPos - (dy / 200.0))
        elif event.buttons() == Qt.RightButton:
            self.set_x_rotation(self.widget.xWorldRot + dy)
            self.set_z_rotation(self.widget.zWorldRot - dx)

        self.lastPos = QPoint(event.pos())

    def wheelEvent(self, event):
        self.widget.zWorldPos += (event.angleDelta().y() / 120)
