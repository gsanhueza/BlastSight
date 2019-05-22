#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from View.GUI.openglwidget import OpenGLWidget


class StandaloneViewer(OpenGLWidget):
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.command_queue = []

        super().__init__()
        self.setWindowTitle('MineVis (Standalone)')

        # FIXME If we set attributes correctly, we shouldn't need this before showing the viewer
        super().show()
        super().hide()

    def show_drawable(self, id_: int) -> None:
        self.command_queue.append(lambda this: OpenGLWidget.show_drawable(this, id_))

    def hide_drawable(self, id_: int) -> None:
        self.command_queue.append(lambda this: OpenGLWidget.hide_drawable(this, id_))

    def delete(self, id_: int) -> None:
        self.command_queue.append(lambda this: OpenGLWidget.delete(this, id_))

    def toggle_wireframe(self, id_: int) -> None:
        self.command_queue.append(lambda this: OpenGLWidget.toggle_wireframe(this, id_))

    def show(self):
        super().show()

        # Apply commands in queue
        for command in self.command_queue:
            command(self)

        sys.exit(self.app.exec_())
