#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from .mode import Mode


class MeasurementMode(Mode):
    def __init__(self):
        super().__init__()
        self.name = 'Measurement Mode'
        self.origins = []
        self.rays = []

    def mousePressEvent(self, event, widget):
        if event.buttons() == Qt.LeftButton:
            self.detect_rays(event, widget)
        else:
            self.origins.clear()
            self.rays.clear()

    def detect_rays(self, event, widget):
        ray, origin = widget.ray_from_click(event.pos().x(), event.pos().y(), 1.0)
        self.origins.append(origin)
        self.rays.append(ray)

        if len(self.rays) == 2:
            widget.measure_from_rays(self.origins, self.rays)
            self.origins.clear()
            self.rays.clear()
