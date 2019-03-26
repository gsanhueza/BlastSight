#!/usr/bin/env python

import sys

from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QAction, QWidget, QMainWindow, QFileDialog

from .ui_loader import load_ui

from .openglwidget import OpenGLWidget
from .normalmode import NormalMode
from .drawmode import DrawMode


class MainWindow(QMainWindow):
    def __init__(self, model=None):
        QMainWindow.__init__(self)
        load_ui('View/UI/mainwindow.ui', self)

        ## Model
        self.model = model

        ## Central Widget
        self.widget = OpenGLWidget(parent=self, mode_class=NormalMode)
        self.setCentralWidget(self.widget)

        self.statusBar.showMessage("Ready")

    # Unless explicitly otherwise, slots are connected via Qt Designer
    @Slot()
    def load_mesh_slot(self):
        (filepath, selected_filter) = QFileDialog.getOpenFileName(parent=self, dir=".", filter="DXF Files (*.dxf)")
        self.model.load_mesh(filepath)
        print(filepath)

    @Slot()
    def normal_mode_slot(self):
        self.widget.currentMode = NormalMode(self.widget)

    @Slot()
    def draw_mode_slot(self):
        self.widget.currentMode = DrawMode(self.widget)
