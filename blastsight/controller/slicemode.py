#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtGui import QMouseEvent
from .mode import Mode


class SliceMode(Mode):
    def __init__(self):
        super().__init__()
        self.name = 'Slice Mode'
        self.origins = []
        self.rays = []

    def mousePressEvent(self, event: QMouseEvent, viewer) -> None:
        if event.buttons() == Qt.LeftButton:
            self.detect_rays(event, viewer)
        else:
            self.origins.clear()
            self.rays.clear()

    def detect_rays(self, event: QMouseEvent, viewer) -> None:
        x, y, z = [event.pos().x(), event.pos().y(), 1.0]
        self.rays.append(viewer.ray_from_click(x, y, z))
        self.origins.append(viewer.origin_from_click(x, y, z))

        if len(self.rays) == 2:
            viewer.slice_from_rays(self.origins, self.rays)
            self.origins.clear()
            self.rays.clear()
