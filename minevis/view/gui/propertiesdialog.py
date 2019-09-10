#!/usr/bin/env python

import numpy as np
import json
import pathlib

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog
from qtpy.QtWidgets import QDialogButtonBox
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
        for i in element.headers:
            self.comboBox_x.addItem(i)
            self.comboBox_y.addItem(i)
            self.comboBox_z.addItem(i)
            self.comboBox_values.addItem(i)

        # Fill properties in QTableWidget
        self.tableWidget_properties.setRowCount(len(element.enabled_properties))
        self.tableWidget_properties.setVerticalHeaderLabels(element.enabled_properties)

        for i, k in enumerate(element.enabled_properties):
            v = element.get_property(k)
            item = QTableWidgetItem()
            text = str(v.tolist()) if type(v) is np.ndarray else str(v)
            item.setText(text)
            self.tableWidget_properties.setItem(i, 0, item)

    def accept(self):
        element = self.viewer.get_drawable(self.id).element

        element.x_str = self.comboBox_x.currentText()
        element.y_str = self.comboBox_y.currentText()
        element.z_str = self.comboBox_z.currentText()
        element.value_str = self.comboBox_values.currentText()

        # Parse values in QTableWidget
        for i in range(self.tableWidget_properties.rowCount()):
            k = self.tableWidget_properties.verticalHeaderItem(i).text()
            v = self.tableWidget_properties.item(i, 0).text()
            try:
                element.set_property(k, float(v))
            except ValueError:  # Element might be a list or string
                try:
                    element.set_property(k, json.loads(v))
                except json.decoder.JSONDecodeError:  # Element is a string
                    element.set_property(k, v)
            except KeyError:  # Element clearly is not a property
                print(f'{k} property does not exist.')

        # Recreate the BlockModelGL instance with the "new" data
        self.viewer.update_drawable(self.id)

        super().accept()

    def show(self):
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

    def comboBoxChanged(self, _):
        # We'll disable the OK button unless all the values are set

        x_ready = bool(self.comboBox_x.currentText())
        y_ready = bool(self.comboBox_y.currentText())
        z_ready = bool(self.comboBox_z.currentText())
        val_ready = bool(self.comboBox_values.currentText())

        enable_ok = x_ready and y_ready and z_ready and val_ready

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable_ok)
