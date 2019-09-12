#!/usr/bin/env python

from qtpy.QtCore import Qt, QPoint
from .mode import Mode


class SliceMode(Mode):
    def __init__(self):
        self.rays = []
        self.lastPos = None
        print("MODE: Slice Mode")

    def mousePressEvent(self, event, widget):
        self.lastPos = QPoint(event.pos())

        if event.buttons() == Qt.LeftButton:
            self.detect_rays(event, widget)
        elif event.buttons() == Qt.RightButton:
            self.rays.clear()

    def mouseMoveEvent(self, event, widget):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        widget.world.setToIdentity()
        if event.buttons() == Qt.MiddleButton:
            distance_x = abs(widget.zCameraPos + widget.zCenterPos) / widget.width()
            distance_y = abs(widget.zCameraPos + widget.zCenterPos) / widget.height()
            self.set_x_movement(widget, widget.xCameraPos - (distance_x * dx))
            self.set_y_movement(widget, widget.yCameraPos + (distance_y * dy))

        self.lastPos = QPoint(event.pos())

    def detect_rays(self, event, widget):
        ray, origin = widget.ray_from_click(event.pos().x(), event.pos().y(), 1.0)
        self.rays.append(ray)

        if len(self.rays) == 2:
            widget.slice_from_rays(self.rays)
            self.rays.clear()
