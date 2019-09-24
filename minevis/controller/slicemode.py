#!/usr/bin/env python

from qtpy.QtCore import Qt
from .mode import Mode


class SliceMode(Mode):
    def __init__(self):
        self.rays = []
        print("MODE: Slice Mode")

    def mousePressEvent(self, event, widget):
        if event.buttons() == Qt.LeftButton:
            self.detect_rays(event, widget)
        else:
            self.rays.clear()

    def detect_rays(self, event, widget):
        ray, _ = widget.ray_from_click(event.pos().x(), event.pos().y(), 1.0)
        self.rays.append(ray)

        if len(self.rays) == 2:
            widget.slice_from_rays(self.rays)
            self.rays.clear()
