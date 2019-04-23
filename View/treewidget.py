#!/usr/bin/env python

from PyQt5.QtCore import *
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QTreeWidget


class TreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.itemClicked.connect(self.single_click)
        self.itemDoubleClicked.connect(self.double_click)
        self.customContextMenuRequested.connect(self.context_menu)

    def context_menu(self, event) -> None:
        """
        Creates a context menu when the user does a right click.

        :param event: Qt Event.
        :return: None
        """
        menu = QMenu(self)

        # Actions
        action_show = QAction('&Show', self)
        action_hide = QAction('&Hide', self)
        action_wireframe = QAction('&Toggle wireframe', self)

        # Icons
        icon = QIcon.fromTheme('show-hidden')
        action_show.setIcon(icon)
        icon = QIcon.fromTheme('object-hidden')
        action_hide.setIcon(icon)
        icon = QIcon.fromTheme('draw-triangle')
        action_wireframe.setIcon(icon)

        # Action commands
        action_show.triggered.connect(lambda: self.show_slot(event))
        action_hide.triggered.connect(lambda: self.hide_slot(event))
        action_wireframe.triggered.connect(lambda: self.wireframe_slot(event))

        menu.addAction(action_show)
        menu.addAction(action_hide)
        menu.addAction(action_wireframe)

        # Pop-up the context menu on current position, but only if an item is there
        if self.itemAt(event):
            menu.popup(QCursor.pos())

    def single_click(self, item, col):
        print('single_click')

    def double_click(self, item):
        print('double_click')

    """
    Slots for context menu
    """
    def show_slot(self, event):
        widget_item = self.itemAt(event)
        widget_item.show()

    def hide_slot(self, event):
        widget_item = self.itemAt(event)
        widget_item.hide()

    def wireframe_slot(self, event):
        widget_item = self.itemAt(event)
        widget_item.toggle_wireframe()
