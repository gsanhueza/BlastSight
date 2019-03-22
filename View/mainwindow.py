#!/usr/bin/env python

import sys

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QAction, QWidget, QMainWindow
from PySide2.QtGui import *

from .openglwidget import OGLWidget
from .normalmode import NormalMode
from .drawmode import DrawMode


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Start")
        self.resize(800, 600)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        # Normal Widget
        normal_widget_action = QAction("Normal mode", self)
        normal_widget_action.setShortcut("Ctrl+N")
        normal_widget_action.triggered.connect(self.normal_mode_slot)

        # Fast Widget
        fast_widget_action = QAction("Draw Mode", self)
        fast_widget_action.setShortcut("Ctrl+D")
        fast_widget_action.triggered.connect(self.draw_mode_slot)

        self.file_menu.addAction(normal_widget_action)
        self.file_menu.addAction(fast_widget_action)
        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Loaded")

        # Central Widget
        widget = OGLWidget(parent=self, mode_class=NormalMode)
        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self, checked):
        sys.exit()

    @Slot()
    def normal_mode_slot(self):
        self.centralWidget().currentMode = NormalMode(self.centralWidget())

    @Slot()
    def draw_mode_slot(self):
        self.centralWidget().currentMode = DrawMode(self.centralWidget())
