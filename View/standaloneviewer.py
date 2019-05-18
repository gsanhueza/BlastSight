#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from View.GUI.openglwidget import OpenGLWidget


class StandaloneViewer(OpenGLWidget):
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.command_queue = []

        super().__init__()
        self.setWindowTitle('MineVis: Stand-alone Viewer')

    def show_element(self, id_: int) -> None:
        self.command_queue.append(lambda this: OpenGLWidget.show_element(this, id_))

    def hide_element(self, id_: int) -> None:
        self.command_queue.append(lambda this: OpenGLWidget.hide_element(this, id_))

    def delete_element(self, id_: int) -> None:
        self.command_queue.append(lambda this: OpenGLWidget.delete_element(this, id_))

    def toggle_wireframe(self, id_: int) -> None:
        self.command_queue.append(lambda this: OpenGLWidget.toggle_wireframe(this, id_))

    def show(self):
        super().show()

        # Apply commands in queue
        for command in self.command_queue:
            command(self)

        sys.exit(self.app.exec_())


viewer = StandaloneViewer()
