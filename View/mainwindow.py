#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from Model.model import Model
from View.treewidgetitem import TreeWidgetItem

from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi('View/UI/mainwindow.ui', self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        self.statusBar.showMessage('Ready')

    def set_model(self, model: Model) -> None:
        self.viewer.set_model(model)

    def fill_tree_widget(self) -> None:
        # Tree widget
        self.treeWidget.clear()

        for id_, gl_drawable in self.viewer.get_gl_collection():
            item = TreeWidgetItem(self.treeWidget, self)
            item.set_element(id_, gl_drawable)
            self.treeWidget.addTopLevelItem(item)

    # Unless explicitly otherwise, slots are connected via Qt Designer
    def load_mesh_slot(self) -> None:
        # TODO Use QSettings (or something) to remember last directory
        (file_path, selected_filter) = QFileDialog.getOpenFileName(
            parent=self,
            directory='.',
            filter='Mesh files (*.dxf *.off);;DXF Files (*.dxf);;OFF Files (*.off)')

        if file_path != '':
            self.load_mesh(file_path)

    def load_mesh(self, file_path: str) -> None:
        if self.viewer.add_mesh(file_path) != -1:
            self.statusBar.showMessage('Mesh loaded')
        else:
            self.statusBar.showMessage('Cannot load mesh')

        self.fill_tree_widget()

    def load_block_model_slot(self) -> None:
        # TODO Use QSettings (or something) to remember last directory
        (file_path, selected_filter) = QFileDialog.getOpenFileName(
            parent=self,
            directory='.',
            filter='CSV Files (*.csv);;All files (*.*)')

        if file_path != '':
            self.load_block_model(file_path)

    def load_block_model(self, file_path: str) -> None:
        if self.viewer.add_block_model(file_path):
            self.statusBar.showMessage('Block model loaded')
        else:
            self.statusBar.showMessage('Cannot load block model')

        self.fill_tree_widget()

    """
    Controller slots
    """
    def normal_mode_slot(self) -> None:
        self.viewer.set_normal_mode()

    def draw_mode_slot(self) -> None:
        self.viewer.set_draw_mode()

    def free_mode_slot(self) -> None:
        self.viewer.set_free_mode()

    def help_slot(self) -> None:
        QMessageBox.information(self,
                                'MineVis - Help',
                                'TO-DO: Create help message box')

    def toggle_wireframe(self, id_: int = 0) -> None:
        try:
            status = self.viewer.toggle_wireframe(id_)
            msg = 'enabled' if status else 'disabled'
            self.statusBar.showMessage(f'Wireframe {id_} {msg}')
        except KeyError:
            msg = 'unavailable'
            self.statusBar.showMessage(f'Wireframe {msg}')

    """
    Overridden events
    """

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        if event.mimeData().hasFormat('text/plain'):
            event.acceptProposedAction()

    def dropEvent(self, event, *args, **kwargs) -> None:
        file_path = event.mimeData().urls()[0].toLocalFile()

        # FIXME We should know beforehand if this is a mesh or a block model
        self.statusBar.showMessage('Loading...')

        if self.viewer.add_mesh(file_path) != -1:
            self.statusBar.showMessage('Mesh loaded')
            self.fill_tree_widget()
            self.viewer.update()
            return
        else:
            self.statusBar.showMessage('Cannot load mesh')

        if self.viewer.add_block_model(file_path) != -1:
            self.statusBar.showMessage('Block model loaded')
            self.fill_tree_widget()
            self.viewer.update()
            return
        else:
            self.statusBar.showMessage('Cannot load block model')

