#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from View.openglwidget import OpenGLWidget
from Model.model import Model


class MineVisViewer(OpenGLWidget):
    # FIXME You still need to queue commands
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()

    def show(self):
        super().show()
        self.toggle_wireframe(0)
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    model = Model()
    input('Before load')
    id_off = model.add_mesh('Model/Mesh/caseron.off')
    input('After load')
    model.update_mesh(id_off, '/home/gabriel/xyzrgb_statuette.off')
    input('After update')
    model.update_mesh(id_off, '/home/gabriel/xyzrgb_statuette.off')
    input('After update')
    model.update_mesh(id_off, '/home/gabriel/xyzrgb_statuette.off')
    input('After update')
    model.delete_mesh(id_off)
    input('After delete')
