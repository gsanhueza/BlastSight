#!/usr/bin/env python

import pathlib

from qtpy import uic
from qtpy.QtCore import Qt
from qtpy.QtCore import QFileInfo
from qtpy.QtCore import QSettings
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QMainWindow
from qtpy.QtWidgets import QMessageBox

from .availablevaluesdialog import AvailableValuesDialog
from .camerapositiondialog import CameraPositionDialog
from .treewidgetitem import TreeWidgetItem


class MineVis(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/mainwindow.ui', self)

        self._settings = QSettings('AMTC', application='MineVis', parent=self)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)
        self.statusBar.showMessage('Ready.')

    @property
    def viewer(self):
        return self.openglwidget

    @property
    def last_dir(self) -> str:
        return self._settings.value('last_directory', '.')

    @last_dir.setter
    def last_dir(self, last_dir: str) -> None:
        self._settings.setValue('last_directory', last_dir)

    def fill_tree_widget(self) -> None:
        # Tree widget
        self.treeWidget.clear()

        for drawable in self.viewer.drawable_collection.values():
            item = TreeWidgetItem(self.treeWidget, self, drawable)
            self.treeWidget.addTopLevelItem(item)
        self.treeWidget.select_item(self.treeWidget.topLevelItemCount(), 0)

    def _load_element(self, method: classmethod, path: str, name: str) -> bool:
        drawable = method(path)
        loaded = bool(drawable)

        if loaded:
            self.statusBar.showMessage(f'{name} loaded.')
        else:
            self.statusBar.showMessage(f'{name} couldn\'t be loaded.')

        return loaded

    def load_mesh(self, file_path: str) -> bool:
        return self._load_element(method=self.viewer.mesh_by_path,
                                  path=file_path,
                                  name='Mesh')

    def load_block_model(self, file_path: str) -> bool:
        status = self._load_element(method=self.viewer.block_model_by_path,
                                    path=file_path,
                                    name='Block model')

        if status:
            self.dialog_available_values(self.viewer.last_id)  # Dialog auto-trigger
        return status

    def load_points(self, file_path: str) -> bool:
        status = self._load_element(method=self.viewer.points_by_path,
                                    path=file_path,
                                    name='Points')

        if status:
            self.dialog_available_values(self.viewer.last_id)  # Dialog auto-trigger
        return status

    def dialog_available_values(self, id_):
        drawable = self.viewer.get_drawable(id_)
        dialog = AvailableValuesDialog(self, drawable)

        dialog.show()

    def dialog_camera_position(self):
        dialog = CameraPositionDialog(self)
        dialog.show()

    """
    Slots. Unless explicitly otherwise, slots are connected via Qt Designer
    """
    def _load_element_slot(self, method: classmethod, filters: str, name: str) -> None:
        (file_paths, selected_filter) = QFileDialog.getOpenFileNames(
            parent=self,
            directory=self.last_dir,
            filter=filters)

        accum = 0

        for file_path in file_paths:
            if file_path != '':
                accum += int(method(file_path))
                self.last_dir = QFileInfo(file_path).absoluteDir().absolutePath()

        if len(file_paths) > 1:
            self.statusBar.showMessage(f'{accum} of {len(file_paths)} {name} loaded.')

    def load_mesh_slot(self) -> None:
        self._load_element_slot(method=self.load_mesh,
                                filters='Mesh Files (*.dxf *.off);;DXF Files (*.dxf);;OFF Files (*.off)',
                                name='meshes')

    def load_block_model_slot(self) -> None:
        self._load_element_slot(method=self.load_block_model,
                                filters='CSV Files (*.csv);;All Files (*.*)',
                                name='block models')

    def load_points_slot(self) -> None:
        self._load_element_slot(method=self.load_points,
                                filters='CSV Files (*.csv);;All Files (*.*)',
                                name='points')

    def normal_mode_slot(self) -> None:
        self.viewer.set_normal_mode()

    def draw_mode_slot(self) -> None:
        self.viewer.set_draw_mode()

    def selection_mode_slot(self) -> None:
        self.viewer.set_selection_mode()

    def help_slot(self) -> None:
        QMessageBox.information(self,
                                'MineVis - Help',
                                'TO-DO: Create help message box')

    """
    Overridden events
    """
    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dropEvent(event, *args, **kwargs)
