#!/usr/bin/env python

import pathlib

from qtpy.QtWidgets import QDialog
from qtpy import uic


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/aboutdialog.ui', self)
