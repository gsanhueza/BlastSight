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

    def autoconnect_to(self, widget):
        self.action_plan_view.triggered.connect(widget.plan_view)
        self.action_north_view.triggered.connect(widget.north_view)
        self.action_east_view.triggered.connect(widget.east_view)
        self.action_take_screenshot.triggered.connect(widget.take_screenshot)
        self.action_take_screenshot.triggered.connect(widget.take_screenshot)
