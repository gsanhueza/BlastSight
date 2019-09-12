#!/usr/bin/env python

from .mode import Mode


class DetectionMode(Mode):
    def __init__(self):
        print("MODE: Detection Mode")

    def mousePressEvent(self, event, widget):
        widget.detect_mesh_intersection(event.pos().x(), event.pos().y(), 1.0)
