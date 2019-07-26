#!/usr/bin/env python

import pathlib

from qtpy import uic
from qtpy.QtCore import Qt
from qtpy.QtCore import QFileInfo
from qtpy.QtCore import QSettings
from qtpy.QtCore import QThreadPool
from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QMessageBox
from qtpy.QtWidgets import QFileDialog

from .availablevaluesdialog import AvailableValuesDialog
from .camerapositiondialog import CameraPositionDialog
from .loadworker import LoadWorker


class Container(QWidget):
    def __init__(self, parent=None, as_lib=False):
        QWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        # Working directory - If this project changes its name (MineVis), change this too
        # package_name = 'MineVis.libraries' if as_lib else 'libraries'
        # uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/container.ui', self, package_name)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/container.ui', self)

        self.threadPool = QThreadPool()
        self._settings = QSettings('AMTC', application='MineVis', parent=self)

    @property
    def viewer(self):
        return self.openglwidget

    @property
    def last_dir(self) -> str:
        return self._settings.value('last_directory', '.')

    @last_dir.setter
    def last_dir(self, last_dir: str) -> None:
        self._settings.setValue('last_directory', last_dir)

    def dialog_available_values(self, id_):
        drawable = self.viewer.get_drawable(id_)
        dialog = AvailableValuesDialog(self, drawable)

        dialog.show()

    def dialog_camera_position(self):
        dialog = CameraPositionDialog(self)
        dialog.show()

    def _load_element(self, method: classmethod, path: str, auto_load=False, *args, **kwargs) -> None:
        worker = LoadWorker(method, path)
        if auto_load:
            worker.signals.loaded.connect(self.dialog_available_values)

        self.threadPool.start(worker)
        self.last_dir = QFileInfo(path).absoluteDir().absolutePath()

    def mesh_by_path(self, file_path: str, *args, **kwargs) -> None:
        self._load_element(method=self.viewer.mesh_by_path,
                           path=file_path, *args, **kwargs)

    def block_model_by_path(self, file_path: str, *args, **kwargs) -> None:
        self._load_element(method=self.viewer.block_model_by_path,
                           path=file_path,
                           auto_load=True, *args, **kwargs)

    def points_by_path(self, file_path: str, *args, **kwargs) -> None:
        self._load_element(method=self.viewer.points_by_path,
                           path=file_path,
                           auto_load=True, *args, **kwargs)

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
        self._load_element_slot(method=self.mesh_by_path,
                                filters='Mesh Files (*.dxf *.off *.h5m);;'
                                        'DXF Files (*.dxf);;'
                                        'OFF Files (*.off);;'
                                        'H5M Files (*.h5m);;'
                                        'All Files (*.*)')

    def load_block_model_slot(self) -> None:
        self._load_element_slot(method=self.block_model_by_path,
                                filters='Data Files (*.csv *.h5p);;'
                                        'CSV Files (*.csv);;'
                                        'H5P Files (*.h5p);;'
                                        'All Files (*.*)')

    def load_points_slot(self) -> None:
        self._load_element_slot(method=self.points_by_path,
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

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dropEvent(event, *args, **kwargs)


class IntegrableContainer(Container):
    def __init__(self, parent=None):
        Container.__init__(self, parent, as_lib=True)

    def mesh_by_path(self, file_path: str, *args, **kwargs) -> None:
        return self.viewer.mesh_by_path(file_path, *args, **kwargs)

    def block_model_by_path(self, file_path: str, *args, **kwargs) -> None:
        return self.viewer.block_model_by_path(file_path, *args, **kwargs)

    def points_by_path(self, file_path: str, *args, **kwargs) -> None:
        return self.viewer.points_by_path(file_path, *args, **kwargs)

    def camera_at(self, id_):
        self.viewer.camera_at(id_)
