#!/usr/bin/env python

from Controller.mode import Mode


class SelectionMode(Mode):
    def __init__(self, widget):
        super().__init__(widget)
        print("MODE: Selection Mode")

    def mousePressEvent(self, event):
        self.widget.detect_intersection(event.pos().x(), event.pos().y(), 1.0)
