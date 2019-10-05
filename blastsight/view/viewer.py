#!/usr/bin/env python

import sys

from qtpy.QtCore import Qt
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QApplication

from .integrableviewer import IntegrableViewer


class Viewer(IntegrableViewer):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.setWindowTitle('BlastSight (Viewer)')

    def show(self, detached: bool = False, timer: int = 0) -> None:
        super().show()

        if detached:
            # This allow us to detach the widget (convenient if running
            # the viewer in an interactive console).
            # WARNING: On PySide2, the viewer WILL freeze when the timer
            # runs out, but you can manually close it with `viewer.close()`.
            QTimer.singleShot(timer, self.app.quit)

        self.app.exec_()

    def take_screenshot(self, save_path=None, width=None, height=None) -> None:
        width = width or self.width()
        height = height or self.height()

        self.resize(width, height)
        super().take_screenshot(save_path)

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        super().dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        super().dropEvent(event, *args, **kwargs)
        self.camera_at(self.last_id)

    def keyPressEvent(self, event) -> None:
        shortcut_commands_dict = {
            Qt.Key_1: lambda: self.plan_view(),
            Qt.Key_2: lambda: self.north_view(),
            Qt.Key_3: lambda: self.east_view(),
            Qt.Key_4: lambda: self.perspective_projection(),
            Qt.Key_5: lambda: self.orthographic_projection(),
            Qt.Key_Delete: lambda: self.delete(self.last_id),
            Qt.Key_Return: lambda: self.fit_to_screen(),
        }

        # Execute command based on event.key()
        shortcut_commands_dict.get(event.key(), lambda: None)()
