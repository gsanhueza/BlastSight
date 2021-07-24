#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtGui import QMouseEvent
from .basecontroller import BaseController


class MeasurementController(BaseController):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.name = 'Measurement'
        self.origins = []
        self.rays = []

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)

        if event.buttons() == Qt.LeftButton:
            self.detect_rays(event)
        else:
            self.origins.clear()
            self.rays.clear()

    def detect_rays(self, event: QMouseEvent) -> None:
        x, y, z = [event.pos().x(), event.pos().y(), 1.0]
        self.rays.append(self.viewer.ray_from_click(x, y, z))
        self.origins.append(self.viewer.origin_from_click(x, y, z))

        if len(self.rays) == 2:
            self.viewer.measure_from_rays(self.origins, self.rays)
            self.origins.clear()
            self.rays.clear()
