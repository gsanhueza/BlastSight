#!/usr/bin/env python

from datetime import datetime

from qtpy.QtCore import Qt
from qtpy.QtCore import QDirIterator
from qtpy.QtCore import QFileInfo
from qtpy.QtCore import QSettings
from qtpy.QtCore import QThreadPool
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QMainWindow
from qtpy.QtWidgets import QTreeWidgetItemIterator
from qtpy.QtWidgets import QHBoxLayout
from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QMenu
from qtpy.QtWidgets import QMenuBar
from qtpy.QtWidgets import QStatusBar
from qtpy.QtWidgets import QDockWidget
from qtpy.QtWidgets import QApplication

from .cameradialog import CameraDialog
from .propertiesdialog import PropertiesDialog
from .colordialog import ColorDialog
from .helpdialog import HelpDialog
from .aboutdialog import AboutDialog
from .loadworker import LoadWorker

from .integrableviewer import IntegrableViewer
from .toolbar import ToolBar
from .treewidget import TreeWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.resize(QApplication.desktop().width() / 2, QApplication.desktop().height() / 2)

        self.centralWidget = QWidget(self)
        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.viewer = IntegrableViewer(self.centralWidget)
        self.horizontalLayout.addWidget(self.viewer)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(self)
        self.menu_File = QMenu('&File', self.menuBar)
        self.menu_Help = QMenu('&Help', self.menuBar)
        self.menu_View = QMenu('&View', self.menuBar)
        self.menu_Tools = QMenu('&Tools', self.menuBar)
        self.setMenuBar(self.menuBar)
        self.toolbar = ToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.dockWidget = QDockWidget(self)
        self.dockWidgetContents = QWidget()
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.treeWidget = TreeWidget(self.dockWidgetContents)
        self.verticalLayout.addWidget(self.treeWidget)
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.addDockWidget(Qt.DockWidgetArea(1), self.dockWidget)

        self.menuBar.addAction(self.menu_File.menuAction())
        self.menuBar.addAction(self.menu_View.menuAction())
        self.menuBar.addAction(self.menu_Tools.menuAction())
        self.menuBar.addAction(self.menu_Help.menuAction())

        self.setWindowTitle('Caseron')
        self.toolbar.setWindowTitle('Show toolbar')
        self.dockWidget.setWindowTitle('Element list')
        self.treeWidget.headerItem().setText(0, 'Elements')

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
        self.toolbar.insertAction(self.toolbar.action_collection.action_plan_view, self.toolbar.action_collection.action_camera_properties)
        self.toolbar.addAction(self.toolbar.action_collection.action_quit)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.generate_menubar()
        self.connect_actions()

        # self.title = self.windowTitle()
        # self.viewer.signal_fps_updated.connect(lambda x: self.setWindowTitle(f'{self.title} (FPS: {x:.1f})'))

    def generate_menubar(self):
        self.menu_File.addAction(self.toolbar.action_collection.action_load_mesh)
        self.menu_File.addAction(self.toolbar.action_collection.action_load_blocks)
        self.menu_File.addAction(self.toolbar.action_collection.action_load_points)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.toolbar.action_collection.action_load_mesh_folder)
        self.menu_File.addAction(self.toolbar.action_collection.action_load_blocks_folder)
        self.menu_File.addAction(self.toolbar.action_collection.action_load_points_folder)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.toolbar.action_collection.action_quit)

        self.menu_View.addAction(self.toolbar.action_collection.action_camera_properties)
        self.menu_View.addAction(self.toolbar.action_collection.action_plan_view)
        self.menu_View.addAction(self.toolbar.action_collection.action_north_view)
        self.menu_View.addAction(self.toolbar.action_collection.action_east_view)
        self.menu_View.addAction(self.toolbar.action_collection.action_fit_to_screen)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.toolbar.action_collection.action_perspective_projection)
        self.menu_View.addAction(self.toolbar.action_collection.action_orthographic_projection)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.toolbar.action_collection.action_take_screenshot)

        self.menu_Tools.addAction(self.toolbar.action_collection.action_slice_mode)
        self.menu_Tools.addAction(self.toolbar.action_collection.action_detection_mode)
        self.menu_Tools.addAction(self.toolbar.action_collection.action_measurement_mode)
        self.menu_Tools.addSeparator()
        self.menu_Tools.addAction(self.toolbar.action_collection.action_normal_mode)

        self.menu_Help.addAction(self.toolbar.action_collection.action_help)
        self.menu_Help.addAction(self.toolbar.action_collection.action_about)

    def connect_actions(self):
        # File
        self.toolbar.action_collection.action_load_mesh.triggered.connect(self.dialog_load_mesh)
        self.toolbar.action_collection.action_load_blocks.triggered.connect(self.dialog_load_blocks)
        self.toolbar.action_collection.action_load_points.triggered.connect(self.dialog_load_points)

        self.toolbar.action_collection.action_load_mesh_folder.triggered.connect(self.dialog_load_mesh_folder)
        self.toolbar.action_collection.action_load_blocks_folder.triggered.connect(self.dialog_load_blocks_folder)
        self.toolbar.action_collection.action_load_points_folder.triggered.connect(self.dialog_load_points_folder)
        self.toolbar.action_collection.action_quit.triggered.connect(self.close)

        # View
        self.toolbar.action_collection.action_camera_properties.triggered.connect(self.dialog_camera)
        self.toolbar.action_collection.action_plan_view.triggered.connect(self.viewer.plan_view)
        self.toolbar.action_collection.action_north_view.triggered.connect(self.viewer.north_view)
        self.toolbar.action_collection.action_east_view.triggered.connect(self.viewer.east_view)
        self.toolbar.action_collection.action_fit_to_screen.triggered.connect(self.viewer.fit_to_screen)
        self.toolbar.action_collection.action_perspective_projection.triggered.connect(self.viewer.perspective_projection)
        self.toolbar.action_collection.action_orthographic_projection.triggered.connect(self.viewer.orthographic_projection)
        self.toolbar.action_collection.action_take_screenshot.triggered.connect(self.dialog_screenshot)

        # Tools
        self.toolbar.action_collection.action_detection_mode.triggered.connect(self.slot_detection_mode)
        self.toolbar.action_collection.action_slice_mode.triggered.connect(self.slot_slice_mode)
        self.toolbar.action_collection.action_measurement_mode.triggered.connect(self.slot_measurement_mode)
        self.toolbar.action_collection.action_normal_mode.triggered.connect(self.slot_normal_mode)

        # Help
        self.toolbar.action_collection.action_help.triggered.connect(self.slot_help)
        self.toolbar.action_collection.action_about.triggered.connect(self.slot_about)

        # Extra actions
        self.toolbar.action_collection.action_show_tree.triggered.connect(self.dockWidget.show)

        self.viewer.signal_mode_updated.connect(self.slot_mode_updated)
        self.viewer.signal_mesh_clicked.connect(self.slot_detected_meshes)
        self.viewer.signal_mesh_distances.connect(self.slot_mesh_distances)
        self.viewer.signal_file_modified.connect(self.fill_tree_widget)

        self.treeWidget.signal_headers_triggered.connect(self.dialog_properties)
        self.treeWidget.signal_colors_triggered.connect(self.dialog_color)
        self.treeWidget.signal_export_mesh.connect(self.dialog_export_mesh)
        self.treeWidget.signal_export_blocks.connect(self.dialog_export_blocks)
        self.treeWidget.signal_export_points.connect(self.dialog_export_points)

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
    def slot_element_loaded(self, _id: int):
        self.statusBar.showMessage(f'Loaded (id: {_id}).')

    def slot_mode_updated(self, mode: str):
        self.statusBar.showMessage(mode)

    def slot_mesh_distances(self, distances: list):
        string_builder = ''
        for _id, distance in distances:
            string_builder += f'(id: {_id}) Distance: {distance}'
            string_builder += '\n'

        self.statusBar.showMessage(string_builder)

    def slot_detected_meshes(self, mesh_ids: list):
        self.treeWidget.clearSelection()
        it = QTreeWidgetItemIterator(self.treeWidget)

        while it.value():
            item = it.value()
            for _id in mesh_ids:
                if _id == item.id:
                    item.setSelected(True)

            it += 1

        self.statusBar.showMessage(f'Detected mesh ids: {mesh_ids}')

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
        worker.signals.loaded.connect(self.slot_element_loaded)

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
    Slots for showing help/about dialogs
    """
    def slot_help(self) -> None:
        HelpDialog(self).exec_()

    def slot_about(self) -> None:
        AboutDialog(self).exec_()

    """
    Events pass-through
    """
    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dropEvent(event, *args, **kwargs)
