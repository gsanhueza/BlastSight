#!/usr/bin/env python

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from View.uiloader import load_ui

from View.openglwidget import OpenGLWidget


class MainWindow(QMainWindow):
    def __init__(self, model=None):
        QMainWindow.__init__(self)
        load_ui('View/UI/mainwindow.ui', self)

        # Central Widget
        self.viewer = OpenGLWidget(parent=self,
                                   model=model)
        self.setCentralWidget(self.viewer)
        self.statusBar.showMessage('Ready')

    # Unless explicitly otherwise, slots are connected via Qt Designer
    @Slot()
    def load_mesh_slot(self):
        # TODO Use QSettings (or something) to remember last directory
        (filepath, selected_filter) = QFileDialog.getOpenFileName(
            parent=self,
            dir='.',
            filter='DXF Files (*.dxf);;OFF Files (*.off);;All files (*.*)')

        if self.viewer.add_mesh(filepath):
            self.statusBar.showMessage('Mesh loaded')
        else:
            self.statusBar.showMessage('Cannot load mesh')

    @Slot()
    def load_block_model_slot(self):
        # TODO Use QSettings (or something) to remember last directory
        (filepath, selected_filter) = QFileDialog.getOpenFileName(
            parent=self,
            dir='.',
            filter='CSV Files (*.csv);;All files (*.*)')

        if self.viewer.add_block_model(filepath):
            self.statusBar.showMessage('Block model loaded')
        else:
            self.statusBar.showMessage('Cannot load block model')

    @Slot()
    def normal_mode_slot(self):
        self.viewer.set_normal_mode()

    @Slot()
    def draw_mode_slot(self):
        self.viewer.set_draw_mode()

    @Slot()
    def free_mode_slot(self):
        self.viewer.set_free_mode()

    @Slot()
    def help_slot(self):
        QMessageBox.information(self,
                                'MineVis - Help',
                                'TO-DO: Create help message box')

    @Slot()
    def toggle_wireframe(self):
        status = self.viewer.toggle_wireframe(0)
        msg = 'enabled' if status else 'disabled'
        self.statusBar.showMessage(f'Wireframe {msg}')
