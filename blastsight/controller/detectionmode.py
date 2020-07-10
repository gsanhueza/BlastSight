#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QMouseEvent
from .mode import Mode


class DetectionMode(Mode):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.name = 'Detection Mode'

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        origin = self.viewer.origin_from_click(event.pos().x(), event.pos().y(), 1.0)
        ray = self.viewer.ray_from_click(event.pos().x(), event.pos().y(), 1.0)

        self.viewer.intersect_meshes(origin, ray)
