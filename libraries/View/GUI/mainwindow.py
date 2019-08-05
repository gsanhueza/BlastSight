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

from .camerapropertiesdialog import CameraPropertiesDialog
from .headersdialog import HeadersDialog
from .colordialog import ColorDialog
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

        # Extra actions
        self.toolbar.insertAction(self.toolbar.action_plan_view, self.toolbar.action_camera_properties)
        self.toolbar.addAction(self.toolbar.action_quit)

        self.generate_menubar()
        self.connect_actions()

        # self._title = self.windowTitle()
        # self.viewer.fps_signal.connect(lambda x: self.setWindowTitle(f'{self._title} (FPS: {x:.1f})'))

    def generate_menubar(self):
        self.menu_File.addAction(self.toolbar.action_load_mesh)
        self.menu_File.addAction(self.toolbar.action_load_block_model)
        self.menu_File.addAction(self.toolbar.action_load_points)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.toolbar.action_quit)

        self.menu_View.addAction(self.toolbar.action_normal_mode)
        self.menu_View.addAction(self.toolbar.action_selection_mode)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.toolbar.action_camera_properties)
        self.menu_View.addAction(self.toolbar.action_plan_view)
        self.menu_View.addAction(self.toolbar.action_north_view)
        self.menu_View.addAction(self.toolbar.action_east_view)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.toolbar.action_take_screenshot)

        self.menu_Help.addAction(self.toolbar.action_help)
        self.menu_Help.addSeparator()

    def connect_actions(self):
        self.toolbar.action_load_mesh.triggered.connect(self.load_mesh_slot)
        self.toolbar.action_load_block_model.triggered.connect(self.load_block_model_slot)
        self.toolbar.action_load_points.triggered.connect(self.load_points_slot)
        self.toolbar.action_quit.triggered.connect(self.close)

        self.toolbar.action_normal_mode.triggered.connect(self.normal_mode_slot)
        self.toolbar.action_selection_mode.triggered.connect(self.selection_mode_slot)

        self.toolbar.action_camera_properties.triggered.connect(self.camera_properties_dialog)
        self.toolbar.action_plan_view.triggered.connect(self.viewer.plan_view)
        self.toolbar.action_north_view.triggered.connect(self.viewer.north_view)
        self.toolbar.action_east_view.triggered.connect(self.viewer.east_view)

        self.toolbar.action_take_screenshot.triggered.connect(self.viewer.take_screenshot)
        self.toolbar.action_show_tree.triggered.connect(self.dockWidget.show)
        self.toolbar.action_help.triggered.connect(self.help_slot)
        self.toolbar.action_quit.triggered.connect(self.close)

        # External widgets
        self.viewer.file_modified_signal.connect(self.fill_tree_widget)
        self.treeWidget.headers_triggered_signal.connect(self.headers_dialog)
        self.treeWidget.colors_triggered_signal.connect(self.color_dialog)

    @property
    def viewer(self):
        return self.openglwidget

    @property
    def toolbar(self):
        return self.mainToolBar

    @property
    def last_dir(self) -> str:
        return self._settings.value('last_directory', '.')

    @last_dir.setter
    def last_dir(self, last_dir: str) -> None:
        self._settings.setValue('last_directory', last_dir)

    def fill_tree_widget(self) -> None:
        self.treeWidget.fill_from_viewer(self.viewer)

    def headers_dialog(self, id_):
        dialog = HeadersDialog(self.viewer, id_)
        dialog.show()

    def color_dialog(self, id_):
        dialog = ColorDialog(self.viewer, id_)
        dialog.show()

    def camera_properties_dialog(self):
        dialog = CameraPropertiesDialog(self.viewer)
        dialog.show()

    def _load_element(self, method: classmethod, path: str, auto_load=False) -> None:
        worker = LoadWorker(method, path)
        if auto_load:
            worker.signals.loaded.connect(self.headers_dialog)

        self.threadPool.start(worker)
        self.last_dir = QFileInfo(path).absoluteDir().absolutePath()

    def load_mesh(self, path: str) -> None:
        self._load_element(method=self.viewer.mesh_by_path,
                           path=path)

    def load_block_model(self, path: str) -> None:
        self._load_element(method=self.viewer.block_model_by_path,
                           path=path,
                           auto_load=True)

    def load_points(self, path: str) -> None:
        self._load_element(method=self.viewer.points_by_path,
                           path=path,
                           auto_load=True)

    """
    Slots. Unless explicitly otherwise, slots are connected via Qt Designer
    """
    def _load_element_slot(self, method: classmethod, filters: str, auto_load=False) -> None:
        (paths, selected_filter) = QFileDialog.getOpenFileNames(
            parent=self,
            directory=self.last_dir,
            filter=filters)

        for path in paths:
            if path != '':
                worker = LoadWorker(method, path)
                if auto_load:
                    worker.signals.loaded.connect(self.headers_dialog)

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

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dropEvent(event, *args, **kwargs)
