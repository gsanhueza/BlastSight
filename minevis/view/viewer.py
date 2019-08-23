#!/usr/bin/env python

import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication
from .gui.integrableviewer import IntegrableViewer


class Viewer(IntegrableViewer):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.setWindowTitle('MineVis (Viewer)')

    def show(self):
        super().show()
        self.app.exec_()

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        super().dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        super().dropEvent(event, *args, **kwargs)
        self.camera_at(self.last_id)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete and self.last_id >= 0:
            self.delete(self.last_id)
        elif event.key() == Qt.Key_T:
            self.take_screenshot()
