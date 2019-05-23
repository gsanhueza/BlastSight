#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from View.GUI.openglwidget import OpenGLWidget


class StandaloneViewer(OpenGLWidget):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.setWindowTitle('MineVis (Standalone)')

    def show(self):
        super().show()
        sys.exit(self.app.exec_())
