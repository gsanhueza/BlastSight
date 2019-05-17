#!/usr/bin/env python

from PyQt5.QtWidgets import QTreeWidgetItem
from View.GUI.availablevaluesdialog import DialogAvailableValues


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, mainwindow=None):
        super().__init__(parent)
        self.mainwindow = mainwindow
        self.gl_element = None

        self.id_: int = None
        self.name: str = None

    def set_element(self, id_: int) -> None:
        self.id_ = id_
        self.gl_element = self.mainwindow.viewer.get_element(self.id_)

        element = self.gl_element.get_model_element()
        self.name = f'{element.name}.{element.ext}'
        self.setText(0, self.name)

    def get_id(self) -> int:
        return self.id_

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> type:
        return type(self.gl_element)

    # Shown in contextual menu
    def show(self) -> None:
        self.gl_element.show()
        self.mainwindow.viewer.update()

    def hide(self) -> None:
        self.gl_element.hide()
        self.mainwindow.viewer.update()

    def remove(self) -> None:
        self.mainwindow.viewer.delete_element(self.id_)
        self.mainwindow.viewer.update()
        self.mainwindow.fill_tree_widget()

    def toggle_wireframe(self) -> None:
        self.gl_element.toggle_wireframe()
        self.mainwindow.viewer.update()

    def update_parameters(self, dialog):
        element = self.gl_element.get_model_element()

        element.x_str = dialog.x
        element.y_str = dialog.y
        element.z_str = dialog.z
        element.value_str = dialog.value

        element.update_coords()
        element.update_values()

        self.mainwindow.viewer.set_centroid(element.centroid)

        # Recreate the BlockModelGL instance with the "new" data
        self.gl_element.setup_vertex_attribs()

    def get_strings(self):
        element = self.gl_element.get_model_element()
        return element.x_str, element.y_str, element.z_str, element.value_str

    def available_values(self) -> None:
        dialog = DialogAvailableValues(self)
        element = self.gl_element.get_model_element()

        for i in element.available_coordinates:
            dialog.comboBox_x.addItem(i)
            dialog.comboBox_y.addItem(i)
            dialog.comboBox_z.addItem(i)

        for i in element.available_values:
            dialog.comboBox_values.addItem(i)

        dialog.show()
