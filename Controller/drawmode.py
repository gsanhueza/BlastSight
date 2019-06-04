#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QVector3D
from PyQt5.QtGui import QVector4D
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

        x = self.lastPos.x()
        y = self.lastPos.y()
        z = 1.0
        ray: QVector3D = self.unproject(x, y, z, self.widget.world, self.widget.camera, self.widget.proj)

        origin = -self.widget.world.column(3).toVector3D()
        d = 0
        n = QVector3D(0.0, 0.0, 1.0).normalized()  # FIXME Calculate from a real figure

        intersection = self.plane_intersection(ray_origin=origin,
                                               ray_direction=ray,
                                               plane_normal=n,
                                               plane_d=d)

        print(f'Intersection at {intersection}')
        print('-------------------------------')

        self.active = False

    def plane_intersection(self, ray_origin, ray_direction, plane_normal, plane_d) -> QVector3D:
        t = (plane_d - QVector3D.dotProduct(plane_normal, ray_origin)) /\
            (QVector3D.dotProduct(plane_normal, ray_direction))

        return ray_origin + t * ray_direction

    def overpaint(self):
        return
        if self.active or True:
            self.widget.painter.begin(self.widget)
            self.widget.painter.setPen(Qt.yellow)
            self.widget.painter.drawText(200, 50, f'Draw enabled = {self.active}')
            self.widget.painter.drawText(200, 70, f'initPos      = {self.initPos}')
            self.widget.painter.drawText(200, 90, f'eventPos     = {self.lastPos}')

            if self.initPos and self.lastPos:
                self.widget.painter.drawLine(self.initPos, self.lastPos)

            self.widget.painter.end()

    def screen_to_normalized(self, _x, _y, _z) -> QVector3D:
        res_x = self.widget.width()
        res_y = self.widget.height()

        x = (2.0 * _x / res_x) - 1.0
        y = 1.0 - (2.0 * _y / res_y)
        z = _z

        return QVector3D(x, y, z)

    # Taken from http://antongerdelan.net/opengl/raycasting.html
    def unproject(self, x, y, z, model, view, proj) -> QVector3D:
        # Step 1
        ray_nds: QVector3D = self.screen_to_normalized(x, y, z)

        # Step 2
        ray_clip: QVector4D = QVector4D(ray_nds.x(), ray_nds.y(), -1.0, 1.0)

        # Step 3
        ray_eye: QVector4D = proj.inverted()[0] * ray_clip
        ray_eye = QVector4D(ray_eye.x(), ray_eye.y(), -1.0, 0.0)

        # Step 4
        ray_wor: QVector3D = ((view * model).inverted()[0] * ray_eye).toVector3D()
        ray_wor.normalize()

        return ray_wor
