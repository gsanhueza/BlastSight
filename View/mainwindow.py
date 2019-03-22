#!/usr/bin/env python

import sys

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QAction, QWidget, QMainWindow
from PySide2.QtGui import *

from .ui_loader import load_ui

from .openglwidget import OpenGLWidget
from .normalmode import NormalMode
from .drawmode import DrawMode


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        load_ui('View/UI/mainwindow.ui', self)

        self.statusBar.showMessage("Ready")

        ## Central Widget
        widget = OpenGLWidget(parent=self, mode_class=NormalMode)
        self.setCentralWidget(widget)

    @Slot()
    def normal_mode_slot(self):
        self.centralWidget.currentMode = NormalMode(self.centralWidget)

    @Slot()
    def draw_mode_slot(self):
        print(type(self.centralWidget))
        self.centralWidget.currentMode = DrawMode(self.centralWidget)
