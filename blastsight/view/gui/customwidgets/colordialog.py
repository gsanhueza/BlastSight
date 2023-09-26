#!/usr/bin/env python

#  Copyright (c) 2019-2023 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QColorDialog, QWidget


class ColorDialog(QColorDialog):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setOption(QColorDialog.ShowAlphaChannel)
        self.setOption(QColorDialog.DontUseNativeDialog, True)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
