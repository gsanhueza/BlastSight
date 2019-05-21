#!/usr/bin/env python

from PyQt5.QtWidgets import QTreeWidgetItem


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, mainwindow=None):
        super().__init__(parent)
        self.mainwindow = mainwindow
        self.gl_element = None

        self.id_: int = None
        self.name: str = None

    def set_element(self, id_: int) -> None:
        self.id_ = id_
        self.gl_element = self.mainwindow.viewer.get_drawable(self.id_)

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
        self.mainwindow.viewer.delete(self.id_)
        self.mainwindow.viewer.update()
        self.mainwindow.fill_tree_widget()

    def toggle_wireframe(self) -> None:
        self.gl_element.toggle_wireframe()
        self.mainwindow.viewer.update()

    def available_values(self) -> None:
        self.mainwindow.show_available_values(self.id_)
