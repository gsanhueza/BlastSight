#!/usr/bin/env python

from PyQt5.QtWidgets import QTreeWidgetItem
from View.GUI.dialog_available_values import DialogAvailableValues


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, mainwindow=None):
        super().__init__(parent)
        self.parent = parent
        self.mainwindow = mainwindow

        self.id_: int = None
        self.name: str = None

    def set_element(self, id_: int) -> None:
        self.id_ = id_

        element = self.mainwindow.viewer.get_element(self.id_).get_model_element()
        self.name = f'{element.name}.{element.ext}'
        self.setText(0, self.name)

    def get_id(self) -> int:
        return self.id_

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> type:
        return type(self.mainwindow.viewer.get_element(self.id_))

    # Shown in contextual menu
    def show(self) -> None:
        self.mainwindow.viewer.get_element(self.id_).show()
        self.mainwindow.viewer.update()

    def hide(self) -> None:
        self.mainwindow.viewer.get_element(self.id_).hide()
        self.mainwindow.viewer.update()

    def remove(self) -> None:
        self.mainwindow.viewer.delete_element(self.id_)
        self.mainwindow.viewer.update()
        self.mainwindow.fill_tree_widget()

    def toggle_wireframe(self) -> None:
        self.mainwindow.viewer.get_element(self.id_).toggle_wireframe()
        self.mainwindow.viewer.update()

    def update_parameters(self, dialog):
        x = dialog.x
        y = dialog.y
        z = dialog.z
        value = dialog.value

        gl_element = self.mainwindow.viewer.get_element(self.id_)
        element = gl_element.get_model_element()

        element.set_x_string(x)
        element.set_y_string(y)
        element.set_z_string(z)
        element.set_value_string(value)

        element.update_coords()
        element.update_values()

        self.mainwindow.viewer.set_centroid(element.get_centroid())

        # Recreate the BlockModelGL instance with the "new" data
        gl_element.setup_vertex_attribs()

    def get_strings(self):
        gl_element = self.mainwindow.viewer.get_element(self.id_)
        element = gl_element.get_model_element()

        x = element.get_x_string()
        y = element.get_y_string()
        z = element.get_z_string()
        val = element.get_value_string()

        return x, y, z, val

    def available_values(self) -> None:
        dialog = DialogAvailableValues(self)
        element = self.mainwindow.viewer.get_element(self.id_).get_model_element()

        for i in element.get_available_coords():
            dialog.comboBox_x.addItem(i)
            dialog.comboBox_y.addItem(i)
            dialog.comboBox_z.addItem(i)

        for i in element.get_available_values():
            dialog.comboBox_values.addItem(i)

        dialog.show()
