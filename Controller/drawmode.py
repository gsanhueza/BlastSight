#!/usr/bin/env python

from PyQt5.QtCore import Qt
from Controller.mode import Mode


class DrawMode(Mode):
    def __init__(self, widget):
        super().__init__(widget)
        print("MODE: Draw Mode")

        self.active = False
        self.initPos = None
        self.lastPos = None

    def mouseMoveEvent(self, event):
        # print("Unable to move in Draw Mode")
        self.lastPos = event.pos()

    def mousePressEvent(self, event):
        self.active = True
        self.initPos = event.pos()
        self.lastPos = event.pos()

    def mouseReleaseEvent(self, event):
        self.lastPos = event.pos()
        self.active = False

    def overpaint(self):
        self.widget.painter.begin(self.widget)
        self.widget.painter.setPen(Qt.yellow)
        self.widget.painter.drawText(200, 50, f'Draw enabled = {self.active}')
        self.widget.painter.drawText(200, 70, f'initPos      = {self.initPos}')
        self.widget.painter.drawText(200, 90, f'eventPos     = {self.lastPos}')

        if self.initPos and self.lastPos:
            self.widget.painter.drawLine(self.initPos, self.lastPos)

        self.widget.painter.end()
