#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
import pathlib

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog
from qtpy.QtWidgets import QTableWidgetItem
from .tools import uic


class PropertiesDialog(QDialog):
    def __init__(self, parent=None, element=None):
        QDialog.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/propertiesdialog.ui', self)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(f'Set properties ({element.name}.{element.extension})')

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
