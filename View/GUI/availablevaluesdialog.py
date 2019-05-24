#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5 import uic


class DialogAvailableValues(QDialog):
    def __init__(self, parent=None, drawable=None):
        QDialog.__init__(self, parent)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)

        uic.loadUi('View/GUI/UI/dialogavailablevalues.ui', self)
        self.parent = parent
        self.drawable = drawable

        self.setWindowTitle(f'Set available values ({drawable.element.name}.{drawable.element.ext})')

    @property
    def element(self):
        return self.drawable.element

    def accept(self):
        self.element.x_str = self.comboBox_x.currentText()
        self.element.y_str = self.comboBox_y.currentText()
        self.element.z_str = self.comboBox_z.currentText()
        self.element.value_str = self.comboBox_values.currentText()

        self.element.update_coords()
        self.element.update_values()

        # Recreate the BlockModelGL instance with the "new" data
        self.parent.viewer.update_drawable(self.element.id)

        super().accept()

    def show(self):
        self.comboBox_x.setCurrentIndex(
            self.comboBox_x.findText(self.element.x_str)
        )
        self.comboBox_y.setCurrentIndex(
            self.comboBox_y.findText(self.element.y_str)
        )
        self.comboBox_z.setCurrentIndex(
            self.comboBox_z.findText(self.element.z_str)
        )
        self.comboBox_values.setCurrentIndex(
            self.comboBox_values.findText(self.element.value_str)
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
