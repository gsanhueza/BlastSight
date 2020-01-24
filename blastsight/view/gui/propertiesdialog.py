#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
import json
import pathlib

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog
from qtpy.QtWidgets import QTableWidgetItem
from qtpy import uic


class PropertiesDialog(QDialog):
    def __init__(self, parent=None, _id=None):
        QDialog.__init__(self, parent)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)

        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/propertiesdialog.ui', self)
        self.viewer = parent
        self.id = _id

        element = self.viewer.get_drawable(self.id).element
        self.setWindowTitle(f'Set properties ({element.name}.{element.extension})')

        # Fill content
        for i in element.all_headers:
            self.comboBox_x.addItem(i)
            self.comboBox_y.addItem(i)
            self.comboBox_z.addItem(i)
            self.comboBox_values.addItem(i)

        # Fill properties in QTableWidget
        self.tableWidget_properties.setRowCount(len(element.customizable_properties))
        self.tableWidget_properties.setVerticalHeaderLabels(element.customizable_properties)

        for i, k in enumerate(element.customizable_properties):
            v = getattr(element, k)
            text = str(v.tolist()) if type(v) is np.ndarray else str(v)
            self.tableWidget_properties.setItem(i, 0, QTableWidgetItem(text))

    def accept(self) -> None:
        element = self.viewer.get_drawable(self.id).element

        # Check alteration of coordinates
        coordinates_altered = not (
            element.x_str == self.comboBox_x.currentText() and
            element.y_str == self.comboBox_y.currentText() and
            element.z_str == self.comboBox_z.currentText()
        )

        element.x_str = self.comboBox_x.currentText()
        element.y_str = self.comboBox_y.currentText()
        element.z_str = self.comboBox_z.currentText()
        element.value_str = self.comboBox_values.currentText()

        # Parse values in QTableWidget
        for i in range(self.tableWidget_properties.rowCount()):
            k = self.tableWidget_properties.verticalHeaderItem(i).text()
            v = self.tableWidget_properties.item(i, 0).text()
            try:
                setattr(element, k, float(v))
            except ValueError:  # Element might be a list or string
                try:  # Element is a list
                    setattr(element, k, json.loads(v))
                except json.decoder.JSONDecodeError:  # Element is a string
                    setattr(element, k, v)
            except KeyError:  # Element clearly is not a property
                print(f'{k} property does not exist.')

        # Recreate the BlockModelGL instance with the "new" data
        self.viewer.update_drawable(self.id)

        # If coordinates were altered and auto-fit is enabled, call fit_to_screen()
        if coordinates_altered and self.viewer.autofit_to_screen:
            self.viewer.fit_to_screen()

        super().accept()

    def show(self) -> None:
        element = self.viewer.get_drawable(self.id).element

        self.comboBox_x.setCurrentIndex(
            self.comboBox_x.findText(element.x_str)
        )
        self.comboBox_y.setCurrentIndex(
            self.comboBox_y.findText(element.y_str)
        )
        self.comboBox_z.setCurrentIndex(
            self.comboBox_z.findText(element.z_str)
        )
        self.comboBox_values.setCurrentIndex(
            self.comboBox_values.findText(element.value_str)
        )

        super().show()
