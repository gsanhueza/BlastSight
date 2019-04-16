#!/usr/bin/env python

from PySide2.QtCore import Qt
from PySide2.QtGui import QVector4D
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

        # if event.button() == Qt.MouseButton.LeftButton:
        #     print("Pressing in Draw Mode with LeftButton")
        # elif event.button() == Qt.MouseButton.MiddleButton:
        #     print("Pressing in Draw Mode with MiddleButton")
        # elif event.button() == Qt.MouseButton.RightButton:
        #     print("Pressing in Draw Mode with RightButton")

    def mouseReleaseEvent(self, event):
        self.lastPos = event.pos()

        P = self.widget.proj
        V = self.widget.camera
        M = self.widget.world

        pos = self.screen_to_normalized(self.lastPos)

        print(f'World coordinates (bad z) = : {pos}')

        # If P * V * M * v = position in screen...
        # M^-1 * V^-1 * P^-1 * P * V * M * v = M^-1 * V^-1 * P^-1 * pos = v
        # With pos = ((2*r_x / res_x) - 1, (2*r_x / res_x) - 1, get_z_depth(), 1.0)
        # That means we need to implement get_z_depth().
        # TODO Multiply/invert/do something to get the world coordinates from the click on screen
        self.active = False

    def overpaint(self):
        if self.active or True:
            self.widget.painter.begin(self.widget)
            self.widget.painter.setPen(Qt.yellow)
            self.widget.painter.drawText(200, 50, f'Draw enabled = {self.active}')
            self.widget.painter.drawText(200, 70, f'initPos      = {self.initPos}')
            self.widget.painter.drawText(200, 90, f'eventPos     = {self.lastPos}')

            if self.initPos and self.lastPos:
                self.widget.painter.drawLine(self.initPos, self.lastPos)

            self.widget.painter.end()

    def screen_to_normalized(self, event_pos):
        res_x = 800  # FIXME Get from screen
        res_y = 530  # FIXME Get from screen

        x = (2 * event_pos.x() / res_x) - 1
        y = (2 * event_pos.y() / res_y) - 1
        z = self.get_z_depth(event_pos)
        w = 1  # Constant

        return QVector4D(x, -y, z, w)

    def get_z_depth(self, event_pos):
        # TODO Get Z depth
        return 0
