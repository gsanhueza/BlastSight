#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QMouseEvent
from .basecontroller import BaseController


class DetectionController(BaseController):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.name = 'Detection'

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)

        x, y, z = [event.pos().x(), event.pos().y(), 1]
        origin = self.viewer.origin_from_click(x, y, z)
        ray = self.viewer.ray_from_click(x, y, z)

        self.viewer.intersect_elements(origin, ray)
