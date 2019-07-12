#!/usr/bin/env python

from qtpy.QtGui import QPainter
from .mode import Mode


class DrawMode(Mode):
    def __init__(self):
        print("MODE: Draw Mode")
        self.active = False
        self.initPos = None
        self.lastPos = None

    def mouseMoveEvent(self, event, widget):
        self.lastPos = event.pos()

    def mousePressEvent(self, event, widget):
        self.active = True
        self.initPos = event.pos()
        self.lastPos = event.pos()

    def mouseReleaseEvent(self, event, widget):
        self.lastPos = event.pos()
        self.active = False

    def overpaint(self, widget):
        painter = QPainter(widget)

        painter.drawText(200, 50, f'Draw enabled = {self.active}')
        painter.drawText(200, 70, f'initPos      = {self.initPos}')
        painter.drawText(200, 90, f'eventPos     = {self.lastPos}')

        if self.initPos and self.lastPos:
            painter.drawLine(self.initPos, self.lastPos)

        painter.end()
