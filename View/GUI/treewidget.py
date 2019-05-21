#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QTreeWidget
from View.Drawables.meshgl import MeshGL
from View.Drawables.blockmodelgl import BlockModelGL


class TreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.itemClicked.connect(self.single_click)
        self.itemDoubleClicked.connect(self.double_click)
        self.customContextMenuRequested.connect(self.context_menu)

        # # Qt documentation states that user types should begin at this value.
        # self.type_mesh = QTreeWidgetItem.UserType
        # self.type_block_model = QTreeWidgetItem.UserType + 1

    def context_menu(self, event) -> None:
        """
        Creates a context menu when the user does a right click.

        :param event: Qt Event.
        :return: None
        """
        # Pop-up the context menu on current position, if an item is there
        item = self.itemAt(event)

        if item:
            self.show_context_menu(item, self.viewport().mapToGlobal(event))

    def show_context_menu(self, item, global_pos):
        menu = QMenu()

        # Actions
        action_show = QAction('&Show', self)
        action_hide = QAction('&Hide', self)
        action_remove = QAction('&Remove', self)
        action_center_camera = QAction('&Center camera', self)
        action_wireframe = QAction('&Toggle wireframe', self)
        action_available_values = QAction('&Available values', self)

        # Icons
        icon = QIcon.fromTheme('show-hidden')
        action_show.setIcon(icon)
        icon = QIcon.fromTheme('object-hidden')
        action_hide.setIcon(icon)
        icon = QIcon.fromTheme('list-remove')
        action_remove.setIcon(icon)
        icon = QIcon.fromTheme('draw-triangle')
        action_wireframe.setIcon(icon)
        icon = QIcon.fromTheme('auto-type')
        action_available_values.setIcon(icon)
        icon = QIcon.fromTheme('camera')
        action_center_camera.setIcon(icon)

        # Action commands
        action_show.triggered.connect(item.show)
        action_hide.triggered.connect(item.hide)
        action_remove.triggered.connect(item.remove)
        action_wireframe.triggered.connect(item.toggle_wireframe)
        action_center_camera.triggered.connect(item.center_camera)
        action_available_values.triggered.connect(item.available_values)

        # Add actions depending on item type
        menu.addAction(action_show)
        menu.addAction(action_hide)
        menu.addAction(action_remove)
        menu.addAction(action_center_camera)

        # FIXME Design a better way to get type of element
        if item.get_type() == MeshGL:
            menu.addAction(action_wireframe)
        elif item.get_type() == BlockModelGL:
            menu.addAction(action_available_values)

        menu.exec_(global_pos)

    def get_item_by_element_id(self, id_: int):
        root = self.invisibleRootItem()
        for i in range(root.childCount()):
            item = root.child(i)
            if item.id_ == id_:
                return item
        return None

    def single_click(self, item, col):
        print('single_click')

    def double_click(self, item):
        print('double_click')
