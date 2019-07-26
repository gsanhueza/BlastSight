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
