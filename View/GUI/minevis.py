#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QFileInfo
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from Model.model import Model
from View.GUI.treewidgetitem import TreeWidgetItem

from PyQt5 import uic


class MineVis(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi('View/UI/mainwindow.ui', self)

        self._settings = QSettings('AMTC', application='MineVis', parent=self)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)
        self.statusBar.showMessage('Ready')

    @property
    def viewer(self):
        return self.openglwidget

    @property
    def model(self) -> Model:
        return self.viewer.model

    @model.setter
    def model(self, model: Model) -> None:
        self.viewer.model = model

    @property
    def last_dir(self) -> str:
        return self._settings.value('last_directory', '.')

    @last_dir.setter
    def last_dir(self, last_dir: str) -> None:
        self._settings.setValue('last_directory', last_dir)

    def fill_tree_widget(self) -> None:
        # Tree widget
        self.treeWidget.clear()

        for id_, gl_drawable in self.viewer.get_gl_collection():
            item = TreeWidgetItem(self.treeWidget, self)
            item.set_element(id_)
            self.treeWidget.addTopLevelItem(item)

    # Unless explicitly otherwise, slots are connected via Qt Designer
    def load_mesh_slot(self) -> None:
        (file_path, selected_filter) = QFileDialog.getOpenFileName(
            parent=self,
            directory=self.last_dir,
            filter='Mesh Files (*.dxf *.off);;'
                   'DXF Files (*.dxf);;'
                   'OFF Files (*.off)')

        if file_path != '':
            self.load_mesh(file_path)
            self.last_dir = QFileInfo(file_path).absoluteDir().absolutePath()

    def load_mesh(self, file_path: str) -> bool:
        loaded = self.viewer.mesh_by_path(file_path) != -1

        if loaded:
            self.statusBar.showMessage('Mesh loaded')
            self.fill_tree_widget()

        return loaded

    def load_block_model_slot(self) -> None:
        (file_path, selected_filter) = QFileDialog.getOpenFileName(
            parent=self,
            directory=self.last_dir,
            filter='CSV Files (*.csv);;All Files (*.*)')

        if file_path != '':
            self.load_block_model(file_path)
            self.last_dir = QFileInfo(file_path).absoluteDir().absolutePath()

    def load_block_model(self, file_path: str) -> bool:
        id_ = self.viewer.block_model_by_path(file_path)
        loaded = id_ != -1

        if loaded:
            self.statusBar.showMessage('Block model loaded')
            self.fill_tree_widget()

            # Auto-trigger of method in TreeWidgetItem
            self.treeWidget.get_item_by_element_id(id_).available_values()

        return loaded

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
        self.statusBar.showMessage('Loading...')

        if self.load_mesh(file_path):
            pass
        elif self.load_block_model(file_path):
            pass
        else:
            self.statusBar.showMessage('Cannot load file')

        self.fill_tree_widget()
        self.viewer.update()
