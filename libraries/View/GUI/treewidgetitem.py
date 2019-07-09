#!/usr/bin/env python

from qtpy.QtWidgets import QTreeWidgetItem


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, mainwindow=None, drawable=None):
        super().__init__(parent)
        self._mainwindow = mainwindow
        self._drawable = drawable

        self.setText(0, f'{self.name}.{self.ext}')

    @property
    def name(self) -> str:
        return self.drawable.element.name

    @property
    def ext(self) -> str:
        return self.drawable.element.ext

    @property
    def type(self) -> type:
        return type(self.drawable)

    @property
    def mainwindow(self):
        return self._mainwindow

    @property
    def drawable(self):
        return self._drawable

    # Shown in contextual menu
    def show(self) -> None:
        self.drawable.show()
        self.mainwindow.viewer.update()

    def hide(self) -> None:
        self.drawable.hide()
        self.mainwindow.viewer.update()

    def delete(self) -> None:
        self.mainwindow.viewer.delete(self.drawable.id)
        self.mainwindow.viewer.update()
        self.mainwindow.fill_tree_widget()

    def toggle_wireframe(self) -> None:
        self.drawable.toggle_wireframe()
        self.mainwindow.viewer.update()

    def toggle_visibility(self) -> None:
        self.drawable.toggle_visibility()
        self.mainwindow.viewer.update()

    def center_camera(self) -> None:
        self.mainwindow.viewer.camera_at(self.drawable.id)

    def available_value_names(self) -> None:
        self.mainwindow.dialog_available_values(self.drawable.id)
