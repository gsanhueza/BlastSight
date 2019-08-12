#!/usr/bin/env python

import pathlib

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog
from qtpy.QtWidgets import QDialogButtonBox
from qtpy import uic


class HeadersDialog(QDialog):
    def __init__(self, parent=None, _id=None):
        QDialog.__init__(self, parent)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)

        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/headersdialog.ui', self)
        self.viewer = parent
        self.id = _id

        element = self.viewer.get_drawable(self.id).element
        self.setWindowTitle(f'Set headers ({element.name}.{element.ext})')

        # Fill content
        for i in element.available_headers:
            self.comboBox_x.addItem(i)
            self.comboBox_y.addItem(i)
            self.comboBox_z.addItem(i)
            self.comboBox_values.addItem(i)

    def accept(self):
        element = self.viewer.get_drawable(self.id).element

        element.x_str = self.comboBox_x.currentText()
        element.y_str = self.comboBox_y.currentText()
        element.z_str = self.comboBox_z.currentText()
        element.value_str = self.comboBox_values.currentText()

        element.update_values()

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