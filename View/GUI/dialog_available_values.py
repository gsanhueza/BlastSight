#!/usr/bin/env python

from PyQt5.QtWidgets import QDialog

from PyQt5 import uic


class DialogAvailableValues(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent.mainwindow)
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
