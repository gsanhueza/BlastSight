#!/usr/bin/env python

from PyQt5.QtWidgets import QDialog

from PyQt5 import uic


class DialogAvailableValues(QDialog):
    def __init__(self, parent=None, gl_element=None):
        QDialog.__init__(self, parent)
        self.gl_element = gl_element
        self.element = gl_element.get_model_element()
        uic.loadUi('View/UI/dialogavailablevalues.ui', self)

    def accept(self):
        x = self.comboBox_x.currentText()
        y = self.comboBox_y.currentText()
        z = self.comboBox_z.currentText()
        value = self.comboBox_values.currentText()

        self.element.set_x_string(x)
        self.element.set_y_string(y)
        self.element.set_z_string(z)
        self.element.set_value_string(value)

        self.element.update_coords()
        self.element.update_values()

        # Recreate the BlockModelGL instance with the "new" data
        self.gl_element.setup_vertex_attribs()
        super().accept()

    def show(self):
        index = self.comboBox_x.findText(self.element.get_x_string())
        self.comboBox_x.setCurrentIndex(index)

        index = self.comboBox_y.findText(self.element.get_y_string())
        self.comboBox_y.setCurrentIndex(index)

        index = self.comboBox_z.findText(self.element.get_z_string())
        self.comboBox_z.setCurrentIndex(index)

        index = self.comboBox_values.findText(self.element.get_value_string())
        self.comboBox_values.setCurrentIndex(index)

        super().show()
