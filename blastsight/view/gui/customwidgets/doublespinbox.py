#!/usr/bin/env python

#  Copyright (c) 2019-2023 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtWidgets import QDoubleSpinBox, QWidget


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self,
                 parent: QWidget,
                 lower: float = -10e6,
                 upper: float = 10e6,
                 decimals: int = 2,
                 step: float = 1.0,
                 width: int = 10) -> None:
        super().__init__(parent)

        self.setMinimum(lower)
        self.setMaximum(upper)
        self.setDecimals(decimals)
        self.setSingleStep(step)
        self.setMinimumWidth(width)
