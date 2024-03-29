#!/usr/bin/env python

#  Copyright (c) 2019-2024 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pathlib

from qtpy.QtWidgets import QDialog
from ..tools import uic


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent.parent}/UI/helpdialog.ui', self)
