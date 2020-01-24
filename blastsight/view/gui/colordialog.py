#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QColor
from qtpy.QtWidgets import QColorDialog


class ColorDialog(QColorDialog):
    def __init__(self, parent=None, _id=None):
        QColorDialog.__init__(self, parent)
        self.setOption(self.ShowAlphaChannel)
        self.setOption(self.DontUseNativeDialog)

        self.viewer = parent
        self.id = _id

        element = self.viewer.get_drawable(self.id).element
        self.setWindowTitle(f'{self.windowTitle()} ({element.name}.{element.extension})')
        self.setCurrentColor(QColor.fromRgb(*[int(255 * x) for x in element.rgba.tolist()]))

    def accept(self) -> None:
        element = self.viewer.get_drawable(self.id).element

        element.color = [self.currentColor().red() / 255,
                         self.currentColor().green() / 255,
                         self.currentColor().blue() / 255]
        element.alpha = self.currentColor().alpha() / 255

        # Recreate the GLDrawable instance with the "new" data
        self.viewer.update_drawable(self.id)

        super().accept()
