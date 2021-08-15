#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtGui import QMouseEvent
from .basecontroller import BaseController


class SliceController(BaseController):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.name = 'Slice'
        self.origins = []
        self.rays = []

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)

        # Setup NDC vertices
        ndc = self.viewer.screen_to_ndc(event.x(), event.y(), 1.0)
        self.viewer.flatline.vertices = [ndc, ndc]
        self.viewer.makeCurrent()
        self.viewer.flatline.reload()

        # Only show line if required
        if len(self.origins) == 0:
            self.viewer.flatline.show()
        else:
            self.viewer.flatline.hide()

        # Discard points if not left-click
        if event.buttons() == Qt.LeftButton:
            self.detect_rays(event)
            self.viewer.setMouseTracking(True)
        else:
            self.origins.clear()
            self.rays.clear()
            self.viewer.setMouseTracking(False)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)

        # Update end of line
        start = self.viewer.flatline.vertices[0]
        ndc = self.viewer.screen_to_ndc(event.x(), event.y(), 1.0)

        self.viewer.flatline.vertices = [start, ndc]
        self.viewer.makeCurrent()
        self.viewer.flatline.reload()

    def detect_rays(self, event: QMouseEvent) -> None:
        x, y, z = [event.pos().x(), event.pos().y(), 1.0]
        self.rays.append(self.viewer.ray_from_click(x, y, z))
        self.origins.append(self.viewer.origin_from_click(x, y, z))

        if len(self.rays) == 2:
            self.viewer.generate_slice_description(self.origins, self.rays)
            self.origins.clear()
            self.rays.clear()
