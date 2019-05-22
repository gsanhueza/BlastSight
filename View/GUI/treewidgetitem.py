#!/usr/bin/env python

from PyQt5.QtWidgets import QTreeWidgetItem


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, mainwindow=None, id_=None, drawable=None):
        super().__init__(parent)
        self.mainwindow = mainwindow
        self.drawable = drawable

        self.id_: int = id_

        element = self.drawable.element
        self.name = f'{element.name}.{element.ext}'
        self.setText(0, self.name)

    def get_id(self) -> int:
        return self.id_

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> type:
        return type(self.drawable)

    # Shown in contextual menu
    def show(self) -> None:
        self.drawable.show()
        self.mainwindow.viewer.update()

    def hide(self) -> None:
        self.drawable.hide()
        self.mainwindow.viewer.update()

    def remove(self) -> None:
        self.mainwindow.viewer.delete(self.id_)
        self.mainwindow.viewer.update()
        self.mainwindow.fill_tree_widget()

    def toggle_wireframe(self) -> None:
        self.drawable.toggle_wireframe()
        self.mainwindow.viewer.update()

    def center_camera(self) -> None:
        element = self.drawable.element
        self.mainwindow.viewer.set_centroid(element.centroid)
        self.mainwindow.viewer.update()

    def available_values(self) -> None:
        self.mainwindow.show_available_values(self.id_)
