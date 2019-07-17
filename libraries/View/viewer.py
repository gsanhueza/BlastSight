#!/usr/bin/env python

import sys

from qtpy.QtWidgets import QApplication
from .GUI.integrableviewer import IntegrableViewer


class Viewer(IntegrableViewer):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.setWindowTitle('MineVis (Viewer)')

    def show(self):
        super().show()
        sys.exit(self.app.exec_())

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        super().dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        super().dropEvent(event, *args, **kwargs)
        self.camera_at(self.last_id)

    def keyPressEvent(self, event):
        import gc
        from qtpy.QtCore import Qt

        if event.key() == Qt.Key_Delete:
            self.delete(self.last_id)
        if event.key() == Qt.Key_End:
            gc.collect()
