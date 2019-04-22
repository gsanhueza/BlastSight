#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from View.openglwidget import OpenGLWidget


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
    viewer = MineVisViewer()
    id_off = viewer.add_mesh('Model/Mesh/caseron.off')
    id_dxf = viewer.add_mesh('Model/Mesh/caseron.dxf')

    viewer.show()
