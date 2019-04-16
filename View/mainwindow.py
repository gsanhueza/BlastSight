#!/usr/bin/env python

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi('View/UI/mainwindow.ui', self)

        self.viewer = self.openGLWidget

        self.statusBar.showMessage('Ready')

    # Unless explicitly otherwise, slots are connected via Qt Designer
    def load_mesh_slot(self):
        # TODO Use QSettings (or something) to remember last directory
        (filepath, selected_filter) = QFileDialog.getOpenFileName(
            parent=self,
            directory='.',
            filter='DXF Files (*.dxf);;OFF Files (*.off);;All files (*.*)')

        if self.viewer.add_mesh(filepath):
            self.statusBar.showMessage('Mesh loaded')
        else:
            self.statusBar.showMessage('Cannot load mesh')

    def load_block_model_slot(self):
        # TODO Use QSettings (or something) to remember last directory
        (filepath, selected_filter) = QFileDialog.getOpenFileName(
            parent=self,
            directory='.',
            filter='CSV Files (*.csv);;All files (*.*)')

        if self.viewer.add_block_model(filepath):
            self.statusBar.showMessage('Block model loaded')
        else:
            self.statusBar.showMessage('Cannot load block model')

    def normal_mode_slot(self):
        self.viewer.set_normal_mode()

    def draw_mode_slot(self):
        self.viewer.set_draw_mode()

    def free_mode_slot(self):
        self.viewer.set_free_mode()

    def help_slot(self):
        QMessageBox.information(self,
                                'MineVis - Help',
                                'TO-DO: Create help message box')

    def toggle_wireframe(self):
        status = self.viewer.toggle_wireframe(0)
        msg = 'enabled' if status else 'disabled'
        self.statusBar.showMessage(f'Wireframe {msg}')
