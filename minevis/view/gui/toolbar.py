#!/usr/bin/env python

import pathlib

from qtpy import uic
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QToolBar


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        QToolBar.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/toolbar.ui', self)

        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setAcceptDrops(True)

    def connect_tree(self, tree):
        self.action_show_tree.triggered.connect(tree.show)

    def connect_viewer(self, viewer):
        self.action_plan_view.triggered.connect(viewer.plan_view)
        self.action_north_view.triggered.connect(viewer.north_view)
        self.action_east_view.triggered.connect(viewer.east_view)
        self.action_show_all.triggered.connect(viewer.show_all)
        self.action_take_screenshot.triggered.connect(viewer.take_screenshot)
