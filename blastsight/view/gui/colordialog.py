#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QColor
from qtpy.QtWidgets import QColorDialog


class ColorDialog(QColorDialog):
    def __init__(self, parent=None, element=None):
        QColorDialog.__init__(self, parent)
        self.setOption(self.ShowAlphaChannel)
        self.setOption(self.DontUseNativeDialog)

        self.setWindowTitle(f'{self.windowTitle()} ({element.name}.{element.extension})')
        self.setCurrentColor(QColor.fromRgb(*[int(255 * x) for x in element.rgba.tolist()]))
