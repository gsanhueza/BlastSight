#!/usr/bin/env python


class Mode:
    def __init__(self, widget):
        self.widget = widget
        self.widget.update()

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def wheelEvent(self, event):
        pass
