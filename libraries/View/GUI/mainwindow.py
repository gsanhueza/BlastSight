#!/usr/bin/env python

import pathlib

from qtpy import uic
from qtpy.QtCore import Qt
from qtpy.QtCore import QFileInfo
from qtpy.QtCore import QSettings
from qtpy.QtCore import QThreadPool
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QMainWindow
from qtpy.QtWidgets import QMessageBox

from .availablevaluesdialog import AvailableValuesDialog
from .camerapositiondialog import CameraPositionDialog
from .treewidgetitem import TreeWidgetItem
from .loadworker import LoadWorker


class MineVis(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/mainwindow.ui', self)

        self._settings = QSettings('AMTC', application='MineVis', parent=self)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)
        self.statusBar.showMessage('Ready')
        self.threadPool = QThreadPool()

        self.generate_toolbar()

    def generate_toolbar(self):
        self.mainToolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.mainToolBar.addAction(self.action_Load_mesh)
        self.mainToolBar.addAction(self.action_Load_block_model)
        self.mainToolBar.addAction(self.action_Load_points)

        self.mainToolBar.addSeparator()

        self.mainToolBar.addAction(self.action_Plan_view)
        self.mainToolBar.addAction(self.action_North_view)
        self.mainToolBar.addAction(self.action_East_view)
        self.mainToolBar.addAction(self.action_Take_screenshot)

        self.mainToolBar.addSeparator()

        self.mainToolBar.addAction(self.action_Quit)

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

    def dialog_available_values(self, id_):
        drawable = self.viewer.get_drawable(id_)
        dialog = AvailableValuesDialog(self, drawable)

        dialog.show()

    def dialog_camera_position(self):
        dialog = CameraPositionDialog(self)
        dialog.show()

    def _load_element(self, method: classmethod, path: str, auto_load=False) -> None:
        worker = LoadWorker(method, path)
        if auto_load:
            worker.signals.loaded.connect(self.dialog_available_values)

        self.threadPool.start(worker)
        self.last_dir = QFileInfo(path).absoluteDir().absolutePath()

    def load_mesh(self, file_path: str) -> None:
        self._load_element(method=self.viewer.mesh_by_path,
                           path=file_path)

    def load_block_model(self, file_path: str) -> None:
        self._load_element(method=self.viewer.block_model_by_path,
                           path=file_path,
                           auto_load=True)

    def load_points(self, file_path: str) -> None:
        self._load_element(method=self.viewer.points_by_path,
                           path=file_path,
                           auto_load=True)

    """
    Slots. Unless explicitly otherwise, slots are connected via Qt Designer
    """
    def _load_element_slot(self, method: classmethod, filters: str, auto_load=False) -> None:
        (file_paths, selected_filter) = QFileDialog.getOpenFileNames(
            parent=self,
            directory=self.last_dir,
            filter=filters)

        for path in file_paths:
            if path != '':
                worker = LoadWorker(method, path)
                if auto_load:
                    worker.signals.loaded.connect(self.dialog_available_values)

                self.threadPool.start(worker)

    def load_mesh_slot(self) -> None:
        self._load_element_slot(method=self.load_mesh,
                                filters='Mesh Files (*.dxf *.off *.h5m);;'
                                        'DXF Files (*.dxf);;'
                                        'OFF Files (*.off);;'
                                        'H5M Files (*.h5m);;'
                                        'All Files (*.*)')

    def load_block_model_slot(self) -> None:
        self._load_element_slot(method=self.load_block_model,
                                filters='Data Files (*.csv *.h5p);;'
                                        'CSV Files (*.csv);;'
                                        'H5P Files (*.h5p);;'
                                        'All Files (*.*)')

    def load_points_slot(self) -> None:
        self._load_element_slot(method=self.load_points,
                                filters='Data Files (*.csv *.h5p);;'
                                        'CSV Files (*.csv);;'
                                        'H5P Files (*.h5p);;'
                                        'All Files (*.*)')

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
