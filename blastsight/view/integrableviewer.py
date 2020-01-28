#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
import traceback

from OpenGL.GL import *

from qtpy.QtCore import QPoint
from qtpy.QtCore import Signal
from qtpy.QtCore import QFileInfo
from qtpy.QtGui import QMatrix4x4
from qtpy.QtGui import QPixmap
from qtpy.QtGui import QRegion
from qtpy.QtGui import QVector4D
from qtpy.QtWidgets import QOpenGLWidget

from .collections.glaxiscollection import GLAxisCollection
from .collections.glbackgroundcollection import GLBackgroundCollection
from .collections.gldrawablecollection import GLDrawableCollection

from .drawables.gldrawable import GLDrawable
from .drawables.axisgl import AxisGL
from .drawables.backgroundgl import BackgroundGL
from .drawables.blockgl import BlockGL
from .drawables.linegl import LineGL
from .drawables.meshgl import MeshGL
from .drawables.pointgl import PointGL
from .drawables.tubegl import TubeGL

from .fpscounter import FPSCounter

from ..controller.detectionmode import DetectionMode
from ..controller.normalmode import NormalMode
from ..controller.slicemode import SliceMode
from ..controller.measurementmode import MeasurementMode

from ..model import utils
from ..model.model import Model


class IntegrableViewer(QOpenGLWidget):
    # Signals
    signal_file_modified = Signal()
    signal_load_success = Signal(int)
    signal_load_failure = Signal()
    signal_export_success = Signal(int)
    signal_export_failure = Signal()

    signal_mesh_clicked = Signal(object)
    signal_mesh_distances = Signal(object)
    signal_mesh_sliced = Signal(object)
    signal_blocks_sliced = Signal(object)

    signal_mode_updated = Signal(str)
    signal_fps_updated = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        # Model
        self.model = Model()

        # Drawable elements
        self.axis_collection = GLAxisCollection(self)
        self.background_collection = GLBackgroundCollection(self)
        self.drawable_collection = GLDrawableCollection(self)

        self.axis = AxisGL(id='AXIS')
        self.axis.add_observer(self)
        self.axis_collection.add(self.axis)

        self.bg = BackgroundGL(id='BG')
        self.bg.add_observer(self)
        self.background_collection.add(self.bg)

        # Signals for viewer (self)
        self.signal_mode_updated.connect(lambda m: print(f'MODE: {m}'))
        self.signal_file_modified.connect(self.recreate)

        # Controllers
        self.current_mode = None
        self.controllers = {}

        self.add_controller(NormalMode, 'normal')
        self.add_controller(DetectionMode, 'detection')
        self.add_controller(SliceMode, 'slice')
        self.add_controller(MeasurementMode, 'measurement')
        self.set_normal_mode()

        # Camera/World/Projection
        self.camera = QMatrix4x4()
        self.world = QMatrix4x4()
        self.proj = QMatrix4x4()

        # FPS Counter
        self.fps_counter = FPSCounter()

        # Initial positions and rotations
        self.rotation_center = [0.0, 0.0, 0.0]
        self.rotation_angle = [0.0, 0.0, 0.0]
        self.camera_position = [0.0, 0.0, 200.0]

        # Extra information
        self._turbo_rendering = False
        self._autofit_to_screen = False

        self.fov = 45.0
        self.smoothness = 2.0  # Bigger => smoother (but slower) rotations
        self.projection_mode = 'perspective'  # 'perspective'/'orthographic'

    """
    Properties
    """
    @property
    def last_id(self) -> int:
        return self.drawable_collection.last_id

    @property
    def last_drawable(self) -> GLDrawable:
        return self.get_drawable(self.last_id)

    @property
    def off_center(self) -> np.ndarray:
        return self.camera_position - self.rotation_center

    @property
    def camera_position(self) -> np.ndarray:
        return np.array([self.xCameraPos, self.yCameraPos, self.zCameraPos])

    @property
    def rotation_angle(self) -> np.ndarray:
        return np.array([self.xCenterRot, self.yCenterRot, self.zCenterRot])

    @property
    def rotation_center(self) -> np.ndarray:
        return np.array([self.xCenterPos, self.yCenterPos, self.zCenterPos])

    @camera_position.setter
    def camera_position(self, pos: list) -> None:
        self.xCameraPos, self.yCameraPos, self.zCameraPos = pos

    @rotation_angle.setter
    def rotation_angle(self, rot: list) -> None:
        self.xCenterRot, self.yCenterRot, self.zCenterRot = rot

    @rotation_center.setter
    def rotation_center(self, center: list) -> None:
        self.xCenterPos, self.yCenterPos, self.zCenterPos = center

    """
    Turbo/Autofit
    """
    def get_turbo_status(self) -> bool:
        return self._turbo_rendering

    def get_autofit_status(self) -> bool:
        return self._autofit_to_screen

    def set_turbo_status(self, status: bool) -> None:
        if status:
            print('WARNING: Turbo-rendering might leave you without memory!')

        self._turbo_rendering = status
        self.update_turbo()

    def set_autofit_status(self, status: bool) -> None:
        self._autofit_to_screen = status
        self.update_autofit()

    def update_turbo(self) -> None:
        for d in self.get_all_drawables():
            d.is_boostable = self.get_turbo_status()

    def update_autofit(self) -> None:
        if self.get_autofit_status():
            self.fit_to_screen()

    """
    Projections
    """
    def perspective_projection(self) -> None:
        self.projection_mode = 'perspective'
        self.update()

    def orthographic_projection(self) -> None:
        self.projection_mode = 'orthographic'
        self.update()

    """
    Generator methods
    """
    def generate_drawable(self, generator):
        try:
            drawable = generator()
            self.signal_load_success.emit(drawable.id)

            return drawable
        except Exception:
            self.signal_load_failure.emit()
            traceback.print_exc()

            return None

    def generate_mesh(self, generator, *args, **kwargs) -> MeshGL:
        return self.generate_drawable(lambda: MeshGL(generator(*args, **kwargs), *args, **kwargs))

    def generate_blocks(self, generator, *args, **kwargs) -> BlockGL:
        return self.generate_drawable(lambda: BlockGL(generator(*args, **kwargs), *args, **kwargs))

    def generate_points(self, generator, *args, **kwargs) -> PointGL:
        return self.generate_drawable(lambda: PointGL(generator(*args, **kwargs), *args, **kwargs))

    def generate_lines(self, generator, *args, **kwargs) -> LineGL:
        return self.generate_drawable(lambda: LineGL(generator(*args, **kwargs), *args, **kwargs))

    def generate_tubes(self, generator, *args, **kwargs) -> TubeGL:
        return self.generate_drawable(lambda: TubeGL(generator(*args, **kwargs), *args, **kwargs))

    """
    Register methods
    """
    def register_drawable(self, drawable):
        if drawable is not None:
            drawable.add_observer(self)
            self.drawable_collection.add(drawable)
            self.signal_file_modified.emit()

        return drawable

    def register_folder(self, path: str, generator, *args, **kwargs) -> list:
        path_list = self.model.get_paths_from_directory(path)

        # We'll block viewer.register_drawable's signal_file_modified until last item has been loaded.
        self.blockSignals(True)
        loaded = [d for d in [generator(path, *args, **kwargs) for path in path_list] if d is not None]
        self.blockSignals(False)

        # We'll manually emit the signals we didn't emit before.
        if len(loaded) > 0:
            self.signal_file_modified.emit()
            self.signal_load_success.emit(self.last_id)
        else:
            self.signal_load_failure.emit()

        return loaded

    """
    Load methods by arguments
    """
    def mesh(self, *args, **kwargs) -> MeshGL:
        return self.register_drawable(self.generate_mesh(self.model.mesh, *args, **kwargs))

    def blocks(self, *args, **kwargs) -> BlockGL:
        return self.register_drawable(self.generate_blocks(self.model.blocks, *args, **kwargs))

    def points(self, *args, **kwargs) -> PointGL:
        return self.register_drawable(self.generate_points(self.model.points, *args, **kwargs))

    def lines(self, *args, **kwargs) -> LineGL:
        return self.register_drawable(self.generate_lines(self.model.lines, *args, **kwargs))

    def tubes(self, *args, **kwargs) -> TubeGL:
        return self.register_drawable(self.generate_tubes(self.model.tubes, *args, **kwargs))

    """
    Load methods by path
    """
    def mesh_by_path(self, path: str, *args, **kwargs) -> MeshGL:
        return self.register_drawable(self.generate_mesh(self.model.mesh_by_path, path, *args, **kwargs))

    def blocks_by_path(self, path: str, *args, **kwargs) -> BlockGL:
        return self.register_drawable(self.generate_blocks(self.model.blocks_by_path, path, *args, **kwargs))

    def points_by_path(self, path: str, *args, **kwargs) -> PointGL:
        return self.register_drawable(self.generate_points(self.model.points_by_path, path, *args, **kwargs))

    def lines_by_path(self, path: str, *args, **kwargs) -> LineGL:
        return self.register_drawable(self.generate_lines(self.model.lines_by_path, path, *args, **kwargs))

    def tubes_by_path(self, path: str, *args, **kwargs) -> TubeGL:
        return self.register_drawable(self.generate_tubes(self.model.tubes_by_path, path, *args, **kwargs))

    def meshes_by_folder_path(self, path: str, *args, **kwargs) -> list:
        return self.register_folder(path, self.mesh_by_path, *args, **kwargs)

    def blocks_by_folder_path(self, path: str, *args, **kwargs) -> list:
        return self.register_folder(path, self.blocks_by_path, *args, **kwargs)

    def points_by_folder_path(self, path: str, *args, **kwargs) -> list:
        return self.register_folder(path, self.points_by_path, *args, **kwargs)

    def lines_by_folder_path(self, path: str, *args, **kwargs) -> list:
        return self.register_folder(path, self.lines_by_path, *args, **kwargs)

    def tubes_by_folder_path(self, path: str, *args, **kwargs) -> list:
        return self.register_folder(path, self.tubes_by_path, *args, **kwargs)

    """
    Export methods
    """
    def _export_element(self, exporter, path: str, _id: int) -> None:
        try:
            exporter(path, _id)
            self.signal_export_success.emit(_id)
        except Exception:
            self.signal_export_failure.emit()

    def export_mesh(self, path, _id) -> None:
        self._export_element(self.model.export_mesh, path, _id)

    def export_blocks(self, path, _id) -> None:
        self._export_element(self.model.export_blocks, path, _id)

    def export_points(self, path, _id) -> None:
        self._export_element(self.model.export_points, path, _id)

    def export_lines(self, path, _id) -> None:
        self._export_element(self.model.export_lines, path, _id)

    def export_tubes(self, path, _id) -> None:
        self._export_element(self.model.export_tubes, path, _id)

    """
    Drawable manipulation
    """
    def get_drawable(self, _id: int):
        return self.drawable_collection.get(_id)

    def show_drawable(self, _id: int) -> None:
        self.get_drawable(_id).show()

    def hide_drawable(self, _id: int) -> None:
        self.get_drawable(_id).hide()

    def update_drawable(self, _id: int) -> None:
        self.makeCurrent()
        self.get_drawable(_id).setup_attributes()
        self.recreate()

    def delete(self, _id: int) -> None:
        if _id < 0:
            return

        self.makeCurrent()
        self.model.delete(_id)
        self.drawable_collection.delete(_id)
        self.signal_file_modified.emit()

    def recreate(self) -> None:
        self.axis_collection.recreate()
        self.background_collection.recreate()
        self.drawable_collection.recreate()
        self.update()

    def get_all_ids(self) -> list:
        return self.drawable_collection.get_all_ids()

    def get_all_drawables(self) -> list:
        return self.drawable_collection.get_all_drawables()

    def update_all(self) -> None:
        for _id in self.get_all_ids():
            self.update_drawable(_id)

    def clear(self) -> None:
        for _id in self.get_all_ids():
            self.delete(_id)

    """
    Camera handling
    """
    def camera_at(self, _id: int) -> None:
        self.fit_to_bounds(*self.get_drawable(_id).element.bounding_box)
        self.update()

    def plan_view(self) -> None:
        self.rotation_angle = [0.0, 0.0, 0.0]
        self.update()

    def north_view(self) -> None:
        self.rotation_angle = [270.0, 0.0, 270.0]
        self.update()

    def east_view(self) -> None:
        self.rotation_angle = [270.0, 0.0, 0.0]
        self.update()

    def fit_to_bounds(self, min_bound: np.ndarray, max_bound: np.ndarray) -> None:
        center = (min_bound + max_bound) / 2
        self.rotation_center = center
        self.camera_position = center

        # Put the camera in a position that allow us to see between the boundaries.
        # In perspective projection, we need a clever trigonometric calculation.
        md = np.max(np.diff([min_bound, max_bound], axis=0))
        aspect = self.width() / self.height()
        fov_rad = self.fov * np.pi / 180.0
        dist = (md / np.tan(fov_rad / 2) + md) / 2.0
        camera_shift = dist * max(1.0, 1.0 / aspect)

        # But in orthographic projection, it's more direct.
        if self.projection_mode == 'orthographic':
            dist = md / 2
            camera_shift = dist * max(1.0, aspect)

        self.zCameraPos += 1.1 * camera_shift
        self.update()

    def fit_to_screen(self) -> None:
        drawables = [d for d in self.get_all_drawables() if d.is_visible]

        if len(drawables) == 0:
            return

        min_all = np.inf * np.ones(3)
        max_all = -np.inf * np.ones(3)

        for drawable in drawables:
            min_bound, max_bound = drawable.element.bounding_box
            min_all = np.min((min_all, min_bound), axis=0)
            max_all = np.max((max_all, max_bound), axis=0)

        self.fit_to_bounds(min_all, max_all)
        self.update()

    """
    Internal methods
    """
    def initializeGL(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_POINT_SPRITE)
        glDisable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self) -> None:
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.world.setToIdentity()
        self.camera.setToIdentity()
        self.proj.setToIdentity()

        # Translate by rotation center (world position)
        self.world.translate(*self.rotation_center)

        # Allow rotation of the world
        self.world.rotate(self.xCenterRot, 1.0, 0.0, 0.0)
        self.world.rotate(self.yCenterRot, 0.0, 1.0, 0.0)
        self.world.rotate(self.zCenterRot, 0.0, 0.0, 1.0)

        # Restore world
        self.world.translate(*-self.rotation_center)

        # Translate the camera
        self.camera.translate(*-self.camera_position)

        # Project (Perspective/Orthographic)
        self.resizeGL(self.width(), self.height())

        # Draw every GLDrawable (meshes, blocks, points, etc)
        glEnable(GL_BLEND)
        self.background_collection.draw(self.proj, self.camera, self.world)
        self.drawable_collection.draw(self.proj, self.camera, self.world)
        self.axis_collection.draw(self.proj, self.camera, self.world)

        # Tick FPS counter
        self.fps_counter.tick(callback=self.signal_fps_updated.emit)

    def resizeGL(self, w: float, h: float) -> None:
        if self.projection_mode == 'perspective':
            self.proj.perspective(self.fov, (w / h), 1.0, 100000.0)
        elif self.projection_mode == 'orthographic':
            z = self.off_center[2]
            aspect = w / h
            self.proj.ortho(-z, z, -z / aspect, z / aspect, 0.0, 100000.0)

    """
    Utilities
    """
    def get_pixmap(self) -> QPixmap:
        pixmap = QPixmap(self.size())
        self.render(pixmap, QPoint(), QRegion(self.rect()))
        return pixmap

    def take_screenshot(self, save_path=None) -> None:
        if save_path:
            self.get_pixmap().save(save_path)

    def screen_to_ndc(self, _x, _y, _z) -> np.ndarray:
        # Click at bottom-left of screen => (-1.0, -1.0, z)
        # Click at top-right of screen => (1.0, 1.0, z)
        # But we can't really know where's z, so we just return 1.0
        x = (2.0 * _x / self.width()) - 1.0
        y = 1.0 - (2.0 * _y / self.height())
        z = 1.0
        return np.array([x, y, z])

    def unproject(self, _x, _y, _z, model, view, proj) -> np.ndarray:
        # Adapted from http://antongerdelan.net/opengl/raycasting.html
        x, y, z = self.screen_to_ndc(_x, _y, _z)

        # We'd use `QVector4D(x, y, -1.0, 1.0)`, but PySide2
        # hasn't implemented QMatrix4x4 * QVector4D yet.
        vector = [x, y, -1.0, 1.0]
        temp_matrix = QMatrix4x4(*[e for e in vector for _ in range(4)])

        ray_eye = (proj.inverted()[0] * temp_matrix).column(0)
        ray_eye = QVector4D(ray_eye.x(), ray_eye.y(), -1.0, 0.0)

        # We'd use `ray_eye`, but PySide2
        # hasn't implemented QMatrix4x4 * QVector4D yet.
        vector = [ray_eye.x(), ray_eye.y(), ray_eye.z(), ray_eye.w()]
        temp_matrix = QMatrix4x4(*[e for e in vector for _ in range(4)])

        ray_world = ((view * model).inverted()[0] * temp_matrix).column(0).toVector3D()
        ray = ray_world.normalized()
        return np.array([ray.x(), ray.y(), ray.z()])

    @staticmethod
    def get_origin(model: QMatrix4x4, view: QMatrix4x4) -> np.ndarray:
        origin = (view * model).inverted()[0].column(3).toVector3D()
        return np.array([origin.x(), origin.y(), origin.z()])

    def ray_from_click(self, x: float, y: float, z: float) -> np.ndarray:
        # Perspective projection is straightforward
        if self.projection_mode == 'perspective':
            return self.unproject(x, y, z, self.world, self.camera, self.proj)

        # Orthographic projection "forces" a click in the center
        return self.unproject(self.width() / 2, self.height() / 2, z,
                              self.world, self.camera, self.proj)

    def origin_from_click(self, x: float, y: float, z: float) -> np.ndarray:
        # Perspective projection is straightforward
        if self.projection_mode == 'perspective':
            return self.get_origin(self.world, self.camera)

        # Orthographic projection needs a bit more of vector arithmetic.
        # A click in the center of the screen gives us the perfect ray,
        # by recycling the perspective's un-project method.

        # But if we don't click in the exact center of screen,
        # we need to trick the origin calculation.
        ndc = self.screen_to_ndc(x, y, z)
        aspect = self.width() / self.height()
        aspect_bias = np.array([1.0, 1.0 / aspect, 0.0])

        # The idea is to strategically move the camera by an offset, so that
        # clicking anywhere in the screen will give us the same result as
        # clicking at the exact center of the screen from a shifted camera.
        offset = self.off_center[2] * ndc * aspect_bias

        # Hack to get the origin when the click is not exactly at center of screen.
        self.camera.translate(*-offset)
        origin = self.get_origin(self.world, self.camera)
        self.camera.translate(*offset)

        return origin

    def slice_meshes(self, origin: np.ndarray, plane_normal: np.ndarray) -> None:
        # Slicing all *visible* meshes
        meshes = [m.element for m in self.drawable_collection.filter(MeshGL) if m.is_visible]

        results = self.model.slice_meshes(origin, plane_normal, meshes)
        self.signal_mesh_sliced.emit(results)

    def slice_blocks(self, origin: np.ndarray, plane_normal: np.ndarray) -> None:
        # Slicing all blocks
        blocks = [m.element for m in self.drawable_collection.filter(BlockGL)]

        results = self.model.slice_blocks(origin, plane_normal, blocks)
        self.signal_blocks_sliced.emit(results)

    def slice_drawables(self, origin: np.ndarray, plane_normal: np.ndarray) -> None:
        self.slice_meshes(origin, plane_normal)
        self.slice_blocks(origin, plane_normal)

    def slice_from_rays(self, origin_list: list, ray_list: list) -> None:
        # A plane is created from `origin` and `ray_list`.
        # In perspective projection, the origin is the same.
        origin = origin_list[0]

        if self.projection_mode == 'perspective':
            # Perspective: Same origins, different rays
            plane_normal = np.cross(*ray_list)
        else:
            # Orthographic: Same rays, different origins
            origin_diff = np.diff(origin_list, axis=0)[0]
            plane_normal = np.cross(ray_list[0], origin_diff)

        plane_normal /= np.linalg.norm(plane_normal)

        # Slice drawables
        self.slice_drawables(origin, plane_normal)

        # Auto-exit the slice mode for now
        self.set_normal_mode()

    def measure_from_rays(self, origin_list: list, ray_list: list) -> None:
        meshes = [m.element for m in self.drawable_collection.filter(MeshGL) if m.is_visible]
        results = self.model.measure_from_rays(origin_list, ray_list, meshes)

        self.signal_mesh_distances.emit(results)

    def detect_mesh_intersection(self, x: float, y: float, z: float) -> None:
        ray = self.ray_from_click(x, y, z)
        origin = self.origin_from_click(x, y, z)
        elements = [m.element for m in self.drawable_collection.filter(MeshGL) if m.is_visible]

        attributes_list = []

        for mesh in elements:
            intersections = mesh.intersect_with_ray(origin, ray)
            closest_point = utils.closest_point_to(origin, intersections)
            if closest_point is not None:
                attributes = {**mesh.attributes,
                              'intersections': intersections,
                              'closest_point': closest_point,
                              }
                attributes_list.append(attributes)

        # Emit signal with clicked mesh
        self.signal_mesh_clicked.emit(attributes_list)

    """
    Controller
    """
    def add_controller(self, mode, mode_name: str) -> None:
        self.controllers[mode_name] = mode

    def set_controller(self, mode_name: str) -> None:
        self.current_mode = self.controllers.get(mode_name)()
        self.signal_mode_updated.emit(self.current_mode.name)
        self.update()

    def set_normal_mode(self) -> None:
        self.set_controller('normal')

    def set_detection_mode(self) -> None:
        self.set_controller('detection')

    def set_slice_mode(self) -> None:
        self.set_controller('slice')

    def set_measurement_mode(self) -> None:
        self.set_controller('measurement')

    """
    Events (dependent on current controller)
    """
    def mouseMoveEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseMoveEvent(event, self)
        self.update()

    def mousePressEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mousePressEvent(event, self)
        self.update()

    def mouseDoubleClickEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseDoubleClickEvent(event, self)
        self.update()

    def mouseReleaseEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseReleaseEvent(event, self)
        self.update()

    def wheelEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.wheelEvent(event, self)
        self.update()

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event, *args, **kwargs) -> None:
        for url in event.mimeData().urls():
            path = url.toLocalFile()

            if QFileInfo(path).isDir():
                self.meshes_by_folder_path(path)
            else:
                self.mesh_by_path(path)
