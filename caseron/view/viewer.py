#!/usr/bin/env python

import sys

from qtpy.QtCore import Qt
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QApplication

from .gui.integrableviewer import IntegrableViewer


class Viewer(IntegrableViewer):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.setWindowTitle('Caseron (Viewer)')

    def show(self, detached: bool = False) -> None:
        super().show()

        if detached:
            timer = QTimer()
            timer.timeout.connect(lambda: self.app.quit())
            timer.start(100)

        self.app.exec_()

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        super().dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        super().dropEvent(event, *args, **kwargs)
        self.camera_at(self.last_id)

    def keyPressEvent(self, event) -> None:
        shortcut_commands_dict = {
            Qt.Key_Delete: lambda: self.delete(self.last_id),
            Qt.Key_Return: lambda: self.fit_to_screen(),
        }

        # Execute command based on event.key()
        shortcut_commands_dict.get(event.key(), lambda: None)()
