#!/usr/bin/env python

from PyQt5.QtWidgets import QDialog

from PyQt5 import uic


class DialogAvailableValues(QDialog):
    def __init__(self, parent=None, id_=-1):
        QDialog.__init__(self, parent)
        self.mainwindow = parent
        self.id = id_
        uic.loadUi('View/UI/dialogavailablevalues.ui', self)

    def accept(self):
        x = self.comboBox_x.currentText()
        y = self.comboBox_y.currentText()
        z = self.comboBox_z.currentText()
        value = self.comboBox_values.currentText()

        gl_element = self.mainwindow.viewer.get_element(self.id)
        element = gl_element.get_model_element()

        element.set_x_string(x)
        element.set_y_string(y)
        element.set_z_string(z)
        element.set_value_string(value)

        element.update_coords()
        element.update_values()

        # Recreate the BlockModelGL instance with the "new" data
        gl_element.setup_vertex_attribs()
        super().accept()

    def show(self):
        gl_element = self.mainwindow.viewer.get_element(self.id)
        element = gl_element.get_model_element()

        index = self.comboBox_x.findText(element.get_x_string())
        self.comboBox_x.setCurrentIndex(index)

        index = self.comboBox_y.findText(element.get_y_string())
        self.comboBox_y.setCurrentIndex(index)

        index = self.comboBox_z.findText(element.get_z_string())
        self.comboBox_z.setCurrentIndex(index)

        index = self.comboBox_values.findText(element.get_value_string())
        self.comboBox_values.setCurrentIndex(index)

        super().show()
