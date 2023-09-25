#!/usr/bin/env python

#  Copyright (c) 2019-2023 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QColor
from qtpy.QtWidgets import QPushButton, QWidget


class ColoredButton(QPushButton):
    qcolor = QColor()

    def __init__(self, parent: QWidget, text: str, color: iter) -> None:
        super().__init__(parent)
        self.setText(text)
        self.set_color(color)

    def get_color(self) -> iter:
        """Returns the color as (R, G, B, A), with values between 0.0 and 1.0"""
        return self.qcolor.getRgbF()

    def set_color(self, value: iter) -> None:
        self.set_qcolor(QColor.fromRgbF(*value))

    def set_qcolor(self, value: QColor) -> None:
        self.qcolor = value
        self.setStyleSheet(f'background-color: {self.qcolor.name()}')
        self.update()
