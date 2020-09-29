#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from qtpy.QtCore import Qt
from qtpy.QtWidgets import *


class PropertiesDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Headers
        self.comboBox_x = QComboBox()
        self.comboBox_y = QComboBox()
        self.comboBox_z = QComboBox()
        self.comboBox_values = QComboBox()

        # Properties
        self.spinBox_alpha = self._generate_spinbox(lower=0.0, upper=1.0, step=0.1)
        self.lineEdit_colormap = QLineEdit()
        self.spinBox_vmin = self._generate_spinbox()
        self.spinBox_vmax = self._generate_spinbox()
        self.lineEdit_size = QLineEdit()
        self.comboBox_markers = QComboBox()
        self.checkBox_limits = QCheckBox()

        # Accept/cancel buttons
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Layout
        self.layout = QGridLayout(self)
        self.append_to_grid(0, QLabel('Coordinate X'), self.comboBox_x)
        self.append_to_grid(1, QLabel('Coordinate Y'), self.comboBox_y)
        self.append_to_grid(2, QLabel('Coordinate Z'), self.comboBox_z)
        self.append_to_grid(3, QLabel('Current value'), self.comboBox_values)

        self.append_to_grid(4, self._generate_separator(), self._generate_separator())

        self.append_to_grid(5, QLabel('Alpha'), self.spinBox_alpha)
        self.append_to_grid(6, QLabel('Colormap'), self.lineEdit_colormap)
        self.append_to_grid(7, QLabel('Vmin'), self.spinBox_vmin)
        self.append_to_grid(8, QLabel('Vmax'), self.spinBox_vmax)
        self.append_to_grid(9, QLabel('Size'), self.lineEdit_size)

        # Space for marker will be enabled by a method

        self.append_to_grid(11, QLabel('Re-calculate limits'), self.checkBox_limits)
        self.append_to_grid(12, QWidget(), self.buttonBox)

        # Signal handling for limits checkbox
        def handle_limits_enabled(status: bool) -> None:
            self.spinBox_vmin.setDisabled(status)
            self.spinBox_vmax.setDisabled(status)
            self.lineEdit_size.setDisabled(status)

        self.checkBox_limits.clicked.connect(handle_limits_enabled)

    def _generate_separator(self) -> QFrame:
        line_separator = QFrame(self)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)

        return line_separator

    def _generate_spinbox(self, lower: float = -10e6, upper: float = 10e6,
                          decimals: int = 2, step: float = 1.0) -> QAbstractSpinBox:
        spinbox = QDoubleSpinBox(self)
        spinbox.setMinimum(lower)
        spinbox.setMaximum(upper)
        spinbox.setDecimals(decimals)
        spinbox.setSingleStep(step)
        spinbox.setMinimumWidth(10)

        return spinbox

    def append_to_grid(self, row: int, *widgets) -> None:
        for i, widget in enumerate(widgets):
            self.layout.addWidget(widget, row, i, 1, 1)

    def fill_headers(self, headers: list) -> None:
        for header in headers:
            self.comboBox_x.addItem(header)
            self.comboBox_y.addItem(header)
            self.comboBox_z.addItem(header)
            self.comboBox_values.addItem(header)

    def fill_markers(self, markers: list):
        for marker in markers:
            self.comboBox_markers.addItem(marker)

    def enable_marker(self) -> None:
        self.append_to_grid(10, QLabel('Marker'), self.comboBox_markers)

    """
    Getters/Setters
    """
    def get_current_headers(self) -> list:
        return [self.comboBox_x.currentText(),
                self.comboBox_y.currentText(),
                self.comboBox_z.currentText(),
                self.comboBox_values.currentText()]

    def get_alpha(self) -> float:
        return self.spinBox_alpha.value()

    def get_colormap(self) -> str:
        return self.lineEdit_colormap.text()

    def get_vmin(self) -> float:
        return self.spinBox_vmin.value()

    def get_vmax(self) -> float:
        return self.spinBox_vmax.value()

    def get_size(self) -> list or float:
        def parse_text_list(text: str) -> list:
            return list(map(float, text.strip('[]').split(',')))

        try:
            return float(self.lineEdit_size.text())
        except ValueError:
            return parse_text_list(self.lineEdit_size.text())

    def get_marker(self) -> str:
        return self.comboBox_markers.currentText()

    def is_recalculate_checked(self) -> bool:
        return self.checkBox_limits.isChecked()

    def set_current_headers(self, headers: list) -> None:
        self.comboBox_x.setCurrentIndex(self.comboBox_x.findText(headers[0]))
        self.comboBox_y.setCurrentIndex(self.comboBox_y.findText(headers[1]))
        self.comboBox_z.setCurrentIndex(self.comboBox_z.findText(headers[2]))
        self.comboBox_values.setCurrentIndex(self.comboBox_values.findText(headers[3]))

    def set_alpha(self, value: float) -> None:
        return self.spinBox_alpha.setValue(value)

    def set_colormap(self, value: str) -> None:
        self.lineEdit_colormap.setText(value)

    def set_vmin(self, value: float) -> None:
        self.spinBox_vmin.setValue(value)

    def set_vmax(self, value: float) -> None:
        self.spinBox_vmax.setValue(value)

    def set_size(self, value: list or float) -> None:
        self.lineEdit_size.setText(str(value))

    def set_marker(self, value: str) -> None:
        self.comboBox_markers.setCurrentIndex(self.comboBox_markers.findText(value))
