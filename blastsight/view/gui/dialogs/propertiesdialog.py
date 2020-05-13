#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from qtpy.QtCore import Qt
from qtpy.QtWidgets import *


class PropertiesDialog(QDialog):
    def __init__(self, element, parent=None):
        QDialog.__init__(self, parent)
        self.resize(450, 500)

        self.setWindowTitle(f'Set properties ({element.name}.{element.extension})')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Left side of the dialog
        self.label_x = QLabel('Coordinate X (Easting)', self)
        self.label_y = QLabel('Coordinate Y (Northing)', self)
        self.label_z = QLabel('Coordinate Z (Elevation)', self)
        self.label_values = QLabel('Current value', self)
        self.label_properties = QLabel('Properties', self)

        # Right side of the dialog
        self.comboBox_x = QComboBox(self)
        self.comboBox_y = QComboBox(self)
        self.comboBox_z = QComboBox(self)
        self.comboBox_values = QComboBox(self)
        self.tableWidget_properties = QTableWidget(self)
        self.tableWidget_properties.setColumnCount(1)
        self.tableWidget_properties.setRowCount(0)
        self.tableWidget_properties.setHorizontalHeaderItem(0, QTableWidgetItem('Value'))
        self.tableWidget_properties.horizontalHeader().setStretchLastSection(True)

        # Accept/cancel buttons
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Layout
        self.layout = QGridLayout(self)
        self.append_to_grid(0, self.label_x, self.comboBox_x)
        self.append_to_grid(1, self.label_y, self.comboBox_y)
        self.append_to_grid(2, self.label_z, self.comboBox_z)
        self.append_to_grid(3, self.label_values, self.comboBox_values)
        self.append_to_grid(4, self.label_properties, self.tableWidget_properties)
        self.append_to_grid(5, QWidget(), self.buttonBox)

        # Fill headers and set current ones
        self.fill_headers(element.all_headers)
        self.current_headers = element.headers

        # Fill properties in QTableWidget
        self.tableWidget_properties.setRowCount(len(element.customizable_properties))
        self.tableWidget_properties.setVerticalHeaderLabels(element.customizable_properties)

        for i, k in enumerate(element.customizable_properties):
            v = getattr(element, k)
            text = str(v.tolist()) if type(v) is np.ndarray else str(v)
            self.tableWidget_properties.setItem(i, 0, QTableWidgetItem(text))

    def append_to_grid(self, row: int, left: QWidget, right: QWidget) -> None:
        self.layout.addWidget(left, row, 0, 1, 1)
        self.layout.addWidget(right, row, 1, 1, 1)

    def fill_headers(self, headers: list) -> None:
        for i in headers:
            self.comboBox_x.addItem(i)
            self.comboBox_y.addItem(i)
            self.comboBox_z.addItem(i)
            self.comboBox_values.addItem(i)

    def has_altered_coordinates(self, element) -> bool:
        altered = False
        for e, c in list(zip(element.headers, self.current_headers))[:3]:
            altered |= not (e == c)

        return altered

    @property
    def current_headers(self) -> list:
        return [self.comboBox_x.currentText(),
                self.comboBox_y.currentText(),
                self.comboBox_z.currentText(),
                self.comboBox_values.currentText()]

    @current_headers.setter
    def current_headers(self, headers: list) -> None:
        self.comboBox_x.setCurrentIndex(self.comboBox_x.findText(headers[0]))
        self.comboBox_y.setCurrentIndex(self.comboBox_y.findText(headers[1]))
        self.comboBox_z.setCurrentIndex(self.comboBox_z.findText(headers[2]))
        self.comboBox_values.setCurrentIndex(self.comboBox_values.findText(headers[3]))
