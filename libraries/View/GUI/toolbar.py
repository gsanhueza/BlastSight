#!/usr/bin/env python

import pathlib

from qtpy import uic
from qtpy.QtWidgets import QToolBar


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        QToolBar.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/toolbar.ui', self)

        self.setAcceptDrops(True)
