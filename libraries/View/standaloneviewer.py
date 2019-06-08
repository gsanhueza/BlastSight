#!/usr/bin/env python

import sys

from qtpy.QtWidgets import QApplication
from .GUI.openglwidget import OpenGLWidget


class StandaloneViewer(OpenGLWidget):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.setWindowTitle('MineVis (Standalone)')

    def show(self):
        super().show()
        sys.exit(self.app.exec_())

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event, *args, **kwargs) -> None:
        super().dropEvent(event, *args, **kwargs)
        self.camera_at(self.last_id)
