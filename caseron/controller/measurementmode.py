#!/usr/bin/env python

from qtpy.QtCore import Qt
from .mode import Mode


class MeasurementMode(Mode):
    def __init__(self):
        super().__init__()
        self.name = 'Measurement Mode'
        self.rays = []

    def mousePressEvent(self, event, widget):
        if event.buttons() == Qt.LeftButton:
            self.detect_rays(event, widget)
        else:
            self.rays.clear()

    def detect_rays(self, event, widget):
        ray, _ = widget.ray_from_click(event.pos().x(), event.pos().y(), 1.0)
        self.rays.append(ray)

        if len(self.rays) == 2:
            widget.measure_from_rays(self.rays)
            self.rays.clear()
