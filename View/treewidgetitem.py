#!/usr/bin/env python

from PyQt5.QtWidgets import QTreeWidgetItem


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.id_ = None
        self.name = None

    def set_element(self, id_: int, elem) -> None:
        self.id_ = id_
        self.name = f'{elem.name}.{elem.ext}'
        self.setText(0, self.name)

    def get_id(self) -> int:
        return self.id_

    def get_name(self) -> str:
        return self.name
