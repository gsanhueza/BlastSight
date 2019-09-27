#!/usr/bin/env python

import pathlib

from qtpy import uic
from qtpy.QtCore import Qt
from qtpy.QtCore import QDirIterator
from qtpy.QtCore import QFileInfo
from qtpy.QtCore import QSettings
from qtpy.QtCore import QThreadPool
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QMainWindow
from qtpy.QtWidgets import QMessageBox

from datetime import datetime

from .cameradialog import CameraDialog
from .propertiesdialog import PropertiesDialog
from .colordialog import ColorDialog
from .loadworker import LoadWorker


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/mainwindow.ui', self)

        self.settings = QSettings('Caseron', application='caseron', parent=self)
        self.filters_dict = {
            'mesh': 'Mesh Files (*.dxf *.off *.h5m);;'
                    'DXF Files (*.dxf);;'
                    'OFF Files (*.off);;'
                    'H5M Files (*.h5m);;'
                    'All Files (*.*)',
            'block': 'Data Files (*.csv *.h5p *.out);;'
                     'CSV Files (*.csv);;'
                     'H5P Files (*.h5p);;'
                     'GSLib Files (*.out);;'
                     'All Files (*.*)',
            'point': 'Data Files (*.csv *.h5p *.out);;'
                     'CSV Files (*.csv);;'
                     'H5P Files (*.h5p);;'
                     'GSLib Files (*.out);;'
                     'All Files (*.*)',
        }

        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)
        self.statusBar.showMessage('Ready')
        self.threadPool = QThreadPool()

        # Extra actions
        self.toolbar.insertAction(self.toolbar.action_plan_view, self.toolbar.action_camera_properties)
        self.toolbar.addAction(self.toolbar.action_quit)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.generate_menubar()
        self.connect_actions()

        # self._title = self.windowTitle()
        # self.viewer.signal_fps_updated.connect(lambda x: self.setWindowTitle(f'{self._title} (FPS: {x:.1f})'))

    def generate_menubar(self):
        self.menu_File.addAction(self.toolbar.action_load_mesh)
        self.menu_File.addAction(self.toolbar.action_load_blocks)
        self.menu_File.addAction(self.toolbar.action_load_points)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.toolbar.action_load_mesh_folder)
        self.menu_File.addAction(self.toolbar.action_load_blocks_folder)
        self.menu_File.addAction(self.toolbar.action_load_points_folder)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.toolbar.action_quit)

        self.menu_Tools.addAction(self.toolbar.action_slice_mode)
        self.menu_Tools.addAction(self.toolbar.action_detection_mode)
        self.menu_Tools.addAction(self.toolbar.action_measurement_mode)
        self.menu_Tools.addSeparator()
        self.menu_Tools.addAction(self.toolbar.action_normal_mode)

        self.menu_View.addAction(self.toolbar.action_camera_properties)
        self.menu_View.addAction(self.toolbar.action_plan_view)
        self.menu_View.addAction(self.toolbar.action_north_view)
        self.menu_View.addAction(self.toolbar.action_east_view)
        self.menu_View.addAction(self.toolbar.action_fit_to_screen)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.toolbar.action_take_screenshot)

        self.menu_Help.addAction(self.toolbar.action_help)
        self.menu_Help.addAction(self.toolbar.action_about)

    def connect_actions(self):
        # Main actions
        self.toolbar.action_load_mesh.triggered.connect(self.dialog_load_mesh)
        self.toolbar.action_load_blocks.triggered.connect(self.dialog_load_blocks)
        self.toolbar.action_load_points.triggered.connect(self.dialog_load_points)

        self.toolbar.action_load_mesh_folder.triggered.connect(self.dialog_load_mesh_folder)
        self.toolbar.action_load_blocks_folder.triggered.connect(self.dialog_load_blocks_folder)
        self.toolbar.action_load_points_folder.triggered.connect(self.dialog_load_points_folder)
        self.toolbar.action_quit.triggered.connect(self.close)

        self.toolbar.action_normal_mode.triggered.connect(self.slot_normal_mode)
        self.toolbar.action_detection_mode.triggered.connect(self.slot_detection_mode)
        self.toolbar.action_slice_mode.triggered.connect(self.slot_slice_mode)
        self.toolbar.action_measurement_mode.triggered.connect(self.slot_measurement_mode)

        self.toolbar.action_camera_properties.triggered.connect(self.dialog_camera)
        self.toolbar.action_plan_view.triggered.connect(self.viewer.plan_view)
        self.toolbar.action_north_view.triggered.connect(self.viewer.north_view)
        self.toolbar.action_east_view.triggered.connect(self.viewer.east_view)
        self.toolbar.action_fit_to_screen.triggered.connect(self.viewer.fit_to_screen)

        self.toolbar.action_take_screenshot.triggered.connect(self.dialog_screenshot)
        self.toolbar.action_show_tree.triggered.connect(self.dockWidget.show)

        self.toolbar.action_help.triggered.connect(self.slot_help)
        self.toolbar.action_about.triggered.connect(self.slot_about)

        # Extra actions
        self.viewer.signal_mode_updated.connect(self.statusbar_update_mode)
        self.viewer.signal_mesh_clicked.connect(self.statusbar_update_detected)
        self.viewer.signal_mesh_distances.connect(self.statusbar_update_distances)
        self.viewer.signal_file_modified.connect(self.fill_tree_widget)

        self.treeWidget.signal_headers_triggered.connect(self.dialog_properties)
        self.treeWidget.signal_colors_triggered.connect(self.dialog_color)
        self.treeWidget.signal_export_mesh.connect(self.dialog_export_mesh)
        self.treeWidget.signal_export_blocks.connect(self.dialog_export_blocks)
        self.treeWidget.signal_export_points.connect(self.dialog_export_points)

    @property
    def viewer(self):
        return self.openglwidget

    @property
    def toolbar(self):
        return self.mainToolBar

    @property
    def last_dir(self) -> str:
        return self.settings.value('last_directory', '.')

    @last_dir.setter
    def last_dir(self, _last_dir: str) -> None:
        self.settings.setValue('last_directory', _last_dir)

    def fill_tree_widget(self) -> None:
        self.treeWidget.fill_from_viewer(self.viewer)

    """
    Status bar updates
    """
    def statusbar_update_loaded(self, _id: int):
        self.statusBar.showMessage(f'Loaded (id: {_id}).')

    def statusbar_update_mode(self, mode: str):
        self.statusBar.showMessage(mode)

    def statusbar_update_distances(self, distances: list):
        string_builder = ''
        for _id, distance in distances:
            string_builder += f'(id: {_id}) Distance: {distance}'
            string_builder += '\n'

        self.statusBar.showMessage(string_builder)

    def statusbar_update_detected(self, meshes: list):
        self.statusBar.showMessage(f'Detected mesh ids: {meshes}')

    """
    Utilities dialogs
    """
    def dialog_properties(self, _id: int):
        dialog = PropertiesDialog(self.viewer, _id)
        dialog.show()

    def dialog_color(self, _id: int):
        dialog = ColorDialog(self.viewer, _id)
        dialog.show()

    def dialog_camera(self):
        dialog = CameraDialog(self.viewer)
        dialog.show()

    def dialog_screenshot(self):
        (path, selected_filter) = QFileDialog.getSaveFileName(
            parent=self,
            directory=f'Caseron Screenshot ({datetime.now().strftime("%Y%m%d-%H%M%S")})',
            filter='PNG image (*.png);;')

        if path != '':
            self.viewer.take_screenshot(path)

    """
    Common functionality for loading/exporting
    """
    def _load_element(self, method: classmethod, path: str) -> None:
        self.statusBar.showMessage('Loading...')

        worker = LoadWorker(method, path)
        worker.signals.loaded.connect(self.statusbar_update_loaded)

        self.threadPool.start(worker)

    def _load_mesh(self, path: str) -> None:
        self._load_element(method=self.viewer.mesh_by_path, path=path)

    def _load_blocks(self, path: str) -> None:
        self._load_element(method=self.viewer.blocks_by_path, path=path)

    def _load_points(self, path: str) -> None:
        self._load_element(method=self.viewer.points_by_path, path=path)

    def _dialog_load_element(self, method: classmethod, filters: str) -> None:
        (paths, selected_filter) = QFileDialog.getOpenFileNames(
            parent=self,
            directory=self.last_dir,
            filter=filters)

        path_list = [p for p in paths if p != '']
        for path in sorted(path_list):
            self._load_element(method, path)
            self.last_dir = QFileInfo(path).absoluteDir().absolutePath()

    def _dialog_load_folder(self, method: classmethod) -> None:
        dir_path = QFileDialog.getExistingDirectory(
            parent=self,
            directory=self.last_dir,
            options=QFileDialog.ShowDirsOnly)

        if dir_path == '':
            return

        it = QDirIterator(dir_path, QDirIterator.Subdirectories)
        path_list = []

        while it.hasNext():
            next_path = it.next()
            if QFileInfo(next_path).isFile():
                path_list.append(next_path)

        for path in sorted(path_list):
            self._load_element(method, path)
            self.last_dir = dir_path

    def _dialog_export_element(self, _id: int, filters: str, method: classmethod) -> None:
        (path, selected_filter) = QFileDialog.getSaveFileName(
            parent=self,
            directory=self.viewer.get_drawable(_id).element.name,
            filter=filters)

        if path != '':
            method(path, _id)

    """
    Slots for loading files
    """
    def dialog_load_mesh(self) -> None:
        self._dialog_load_element(method=self._load_mesh,
                                  filters=self.filters_dict.get('mesh'))

    def dialog_load_blocks(self) -> None:
        self._dialog_load_element(method=self._load_blocks,
                                  filters=self.filters_dict.get('block'))

    def dialog_load_points(self) -> None:
        self._dialog_load_element(method=self._load_points,
                                  filters=self.filters_dict.get('point'))

    def dialog_load_mesh_folder(self) -> None:
        self._dialog_load_folder(method=self._load_mesh)

    def dialog_load_blocks_folder(self) -> None:
        self._dialog_load_folder(method=self._load_blocks)

    def dialog_load_points_folder(self) -> None:
        self._dialog_load_folder(method=self._load_points)

    """
    Slots for exporting files
    """
    def dialog_export_mesh(self, _id: int) -> None:
        self._dialog_export_element(_id=_id,
                                    filters='Caseron mesh (*.h5m);;',
                                    method=self.viewer.export_mesh)

    def dialog_export_blocks(self, _id: int) -> None:
        self._dialog_export_element(_id=_id,
                                    filters='Caseron blocks (*.h5p);;',
                                    method=self.viewer.export_blocks)

    def dialog_export_points(self, _id: int) -> None:
        self._dialog_export_element(_id=_id,
                                    filters='Caseron points (*.h5p);;',
                                    method=self.viewer.export_points)

    """
    Slots for modifying controller modes
    """
    def slot_normal_mode(self) -> None:
        self.viewer.set_normal_mode()

    def slot_detection_mode(self) -> None:
        self.viewer.set_detection_mode()

    def slot_slice_mode(self) -> None:
        self.viewer.set_slice_mode()

    def slot_measurement_mode(self) -> None:
        self.viewer.set_measurement_mode()

    """
    Slots for showing help dialogs
    """
    def slot_help(self) -> None:
        QMessageBox.information(self,
                                'Caseron - Help',
                                'TO-DO: Create help message box')

    def slot_about(self) -> None:
        QMessageBox.information(self,
                                'Caseron - About',
                                'TO-DO: Create about message box\n' +
                                'We\'re currently using utilities from:\n' +
                                '- pymesh (cylinder generation)\n' +
                                '- matplotlib (hsv to rgb)\n' +
                                '- flat color icons (from icons8.com)\n' +
                                '- meshcut (slice mesh by a plane)\n' +
                                '- trimesh (volume of a mesh, adapted)\n' +
                                '- colour (parse string to color)'
                                )

    """
    Events pass-through
    """
    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dropEvent(event, *args, **kwargs)
