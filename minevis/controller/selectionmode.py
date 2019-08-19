#!/usr/bin/env python

from .mode import Mode


class SelectionMode(Mode):
    def __init__(self):
        print("MODE: Selection Mode")

    def mousePressEvent(self, event, widget):
        widget.detect_intersection(event.pos().x(), event.pos().y(), 1.0)
