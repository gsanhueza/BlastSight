#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5 import uic


class DialogAvailableValues(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent.mainwindow)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)

        uic.loadUi('View/UI/dialogavailablevalues.ui', self)
        self.parent = parent
        self.x = None
        self.y = None
        self.z = None
        self.value = None

    def accept(self):
        self.x = self.comboBox_x.currentText()
        self.y = self.comboBox_y.currentText()
        self.z = self.comboBox_z.currentText()
        self.value = self.comboBox_values.currentText()

        self.parent.update_parameters(self)

        super().accept()

    def show(self):
        (x, y, z, val) = self.parent.get_strings()

        index = self.comboBox_x.findText(x)
        self.comboBox_x.setCurrentIndex(index)

        index = self.comboBox_y.findText(y)
        self.comboBox_y.setCurrentIndex(index)

        index = self.comboBox_z.findText(z)
        self.comboBox_z.setCurrentIndex(index)

        index = self.comboBox_values.findText(val)
        self.comboBox_values.setCurrentIndex(index)

        super().show()

    def comboBoxChanged(self, _):
        # We'll disable the OK button unless all the values are set

        x_ready = bool(self.comboBox_x.currentText())
        y_ready = bool(self.comboBox_y.currentText())
        z_ready = bool(self.comboBox_z.currentText())
        val_ready = bool(self.comboBox_values.currentText())

        enable_ok = x_ready and y_ready and z_ready and val_ready

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable_ok)
