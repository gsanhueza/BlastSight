#!/usr/bin/env python

from PyQt5.QtWidgets import QTreeWidgetItem
from View.Drawables.gldrawable import GLDrawable
from View.dialog_available_values import DialogAvailableValues


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, mainwindow=None):
        super().__init__(parent)
        self.parent = parent
        self.mainwindow = mainwindow

        self.id_: int = None
        self.name: str = None
        self.gl_elem: GLDrawable = None
        self.model_elem = None

    def set_element(self, id_: int, gl_elem: GLDrawable) -> None:
        self.id_ = id_
        self.gl_elem = gl_elem
        self.model_elem = self.gl_elem.get_model_element()
        self.name = f'{self.model_elem.name}.{self.model_elem.ext}'
        self.setText(0, self.name)

    def get_id(self) -> int:
        return self.id_

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> type:
        return type(self.gl_elem)

    # Shown in contextual menu
    def show(self) -> None:
        self.gl_elem.show()
        self.gl_elem.update()

    def hide(self) -> None:
        self.gl_elem.hide()
        self.gl_elem.update()

    def remove(self) -> None:
        self.mainwindow.viewer.delete_element(self.id_)
        self.mainwindow.viewer.update()
        self.mainwindow.fill_tree_widget()

    def toggle_wireframe(self) -> None:
        self.gl_elem.toggle_wireframe()
        self.gl_elem.update()

    def available_values(self) -> None:
        dialog = DialogAvailableValues(self.parent, self.model_elem)

        for i in self.model_elem.get_available_values():
            dialog.comboBox_x.addItem(i)
            dialog.comboBox_y.addItem(i)
            dialog.comboBox_z.addItem(i)
            dialog.comboBox_values.addItem(i)

        dialog.show()
