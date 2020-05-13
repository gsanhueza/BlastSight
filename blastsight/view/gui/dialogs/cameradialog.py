#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtWidgets import QDialog
from qtpy.QtWidgets import QDialogButtonBox
from qtpy.QtWidgets import QVBoxLayout

from ..camerawidget import CameraWidget


class CameraDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Camera Properties')

        self.camera = CameraWidget(self)
        self.button_box = QDialogButtonBox(self)
        self.button_box.setStandardButtons(QDialogButtonBox.Close)
        self.button_box.clicked.connect(self.close)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.camera)
        self.layout.addWidget(self.button_box)

    def connect_viewer(self, viewer) -> None:
        self.camera.connect_viewer(viewer)
