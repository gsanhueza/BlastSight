#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
import warnings

from OpenGL.GL import *

from qtpy.QtCore import QFileInfo
from qtpy.QtCore import QPoint
from qtpy.QtCore import QTimer
from qtpy.QtCore import Signal
from qtpy.QtGui import QMatrix4x4
from qtpy.QtGui import QPixmap
from qtpy.QtGui import QQuaternion
from qtpy.QtGui import QRegion
from qtpy.QtGui import QVector3D
from qtpy.QtGui import QVector4D
from qtpy.QtWidgets import QOpenGLWidget
from scipy.spatial.transform import Rotation

from .collections.glaxiscollection import GLAxisCollection
from .collections.glbackgroundcollection import GLBackgroundCollection
from .collections.gldrawablecollection import GLDrawableCollection

from .drawables.gldrawable import GLDrawable
from .drawables.blockgl import BlockGL
from .drawables.linegl import LineGL
from .drawables.meshgl import MeshGL
from .drawables.pointgl import PointGL
from .drawables.tubegl import TubeGL

from .drawablefactory import DrawableFactory
from .fpscounter import FPSCounter

from ..controller.mode import Mode
from ..controller.detectionmode import DetectionMode
from ..controller.normalmode import NormalMode
from ..controller.slicemode import SliceMode
from ..controller.measurementmode import MeasurementMode

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
    signal_slice_description = Signal(object)

    signal_process_updated = Signal(int)
    signal_process_started = Signal()
    signal_process_finished = Signal()

    signal_mode_updated = Signal(str)
    signal_fps_updated = Signal(float)

    signal_camera_rotated = Signal(object)
    signal_camera_translated = Signal(object)
    signal_center_translated = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        # Model
        self.model = Model()

        # Factory
        self.factory = DrawableFactory(self.model)

        # Drawable elements
        self.axis_collection = GLAxisCollection(self)
        self.background_collection = GLBackgroundCollection(self)
        self.drawable_collection = GLDrawableCollection(self)

        # Controllers
        self.current_mode = None
        self.controllers = {}

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
        self._turbo = False
        self._autofit = False
        self._animated = False

        self.fov = 45.0
        self.smoothness = 2.0  # Bigger => smoother (but slower) rotations
        self.projection_mode = 'perspective'  # 'perspective'/'orthographic'

        # Initialize viewer
        self.initialize()

    def initialize(self) -> None:
        # Axis/Background
        self.register_drawable(self.factory.axis(), self.axis_collection)
        self.register_drawable(self.factory.background(), self.background_collection)

        # Signals
        self.signal_file_modified.connect(self.recreate)
        self.signal_camera_rotated.connect(self.update)
        self.signal_camera_translated.connect(self.update)
        self.signal_center_translated.connect(self.update)

        # Controllers
        self.add_controller(NormalMode(self))
        self.add_controller(DetectionMode(self))
        self.add_controller(SliceMode(self))
        self.add_controller(MeasurementMode(self))
        self.set_normal_mode()

        # FPSCounter
        self.fps_counter.add_callback(self.signal_fps_updated.emit)

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
    def axis(self) -> GLDrawable:
        return self.axis_collection.get_last()

    # DEPRECATED
    @property
    def bg(self) -> GLDrawable:
        self._deprecated_message('bg', 'background')
        return self.background

    @property
    def background(self) -> GLDrawable:
        return self.background_collection.get_last()

    @property
    def off_center(self) -> np.ndarray:
        return self.camera_position - self.rotation_center

    """
    Camera movements/rotations
    """
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
        self.signal_camera_translated.emit(pos)

    @rotation_angle.setter
    def rotation_angle(self, rot: list) -> None:
        self.xCenterRot, self.yCenterRot, self.zCenterRot = rot
        self.signal_camera_rotated.emit(rot)

    @rotation_center.setter
    def rotation_center(self, center: list) -> None:
        self.xCenterPos, self.yCenterPos, self.zCenterPos = center
        self.signal_center_translated.emit(center)

    """
    API for partial camera movements/rotations
    """
    def translate(self, x: float, y: float, z: float) -> None:
        self.camera_position += np.array([x, y, z])

    def translate_center(self, x: float, y: float, z: float) -> None:
        self.rotation_center += np.array([x, y, z])

    def rotate(self, alpha: float, beta: float, gamma: float) -> None:
        self.rotation_angle += np.array([alpha, beta, gamma])
        self.rotation_angle %= 360

    """
    API for the camera (animated)
    """
    def get_camera_position(self) -> np.ndarray:
        return self.camera_position

    def get_rotation_center(self) -> np.ndarray:
        return self.rotation_center

    def get_rotation_angle(self) -> np.ndarray:
        return self.rotation_angle

    def set_camera_position(self, target) -> None:
        origin = self.get_camera_position()

        def setter(value):
            self.camera_position = value
        self.animate(origin, target, method=setter) if self.is_animated() else setter(target)

    def set_rotation_center(self, target) -> None:
        origin = self.get_rotation_center()

        def setter(value):
            self.rotation_center = value
        self.animate(origin, target, method=setter) if self.is_animated() else setter(target)

    def set_rotation_angle(self, target) -> None:
        # Fix any difference > 180° so the camera doesn't over-rotate
        origin = self.get_rotation_angle() % 360
        origin[origin - target > 180] -= 360
        origin[origin - target < -180] += 360

        def setter(value):
            self.rotation_angle = value
        self.animate(origin, target, method=setter) if self.is_animated() else setter(target)

    """
    Animation / Turbo
    """
    def set_turbo_rendering(self, status: bool) -> None:
        self.blockSignals(True)

        for d in self.get_all_drawables():
            d.is_boostable = status

        self.blockSignals(False)
        self.recreate()

    def is_animated(self) -> bool:
        return self._animated

    def set_animated(self, status: bool) -> None:
        self._animated = status

    def animate(self, start, end, method: callable, steps: int = 20) -> callable:
        timer = QTimer(self)
        linspace = iter(np.linspace(start, end, steps))

        def animation_per_frame():
            try:
                method(next(linspace))
                self.update()
            except StopIteration:
                timer.stop()

        timer.timeout.connect(animation_per_frame)
        timer.start(1.0 / 60.0)

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
    Registration methods
    """
    def register_drawable(self, drawable, collection=None):
        if drawable is None:
            self.signal_load_failure.emit()
            return None

        if collection is None:
            collection = self.drawable_collection

        # Register in collection
        drawable.add_observer(self)
        collection.add(drawable)

        # Emit success signals
        self.signal_file_modified.emit()
        self.signal_load_success.emit(drawable.id)

        return drawable

    """
    Load methods by arguments
    """
    def mesh(self, *args, **kwargs) -> MeshGL:
        return self.register_drawable(self.factory.mesh(*args, **kwargs))

    def blocks(self, *args, **kwargs) -> BlockGL:
        return self.register_drawable(self.factory.blocks(*args, **kwargs))

    def points(self, *args, **kwargs) -> PointGL:
        return self.register_drawable(self.factory.points(*args, **kwargs))

    def lines(self, *args, **kwargs) -> LineGL:
        return self.register_drawable(self.factory.lines(*args, **kwargs))

    def tubes(self, *args, **kwargs) -> TubeGL:
        return self.register_drawable(self.factory.tubes(*args, **kwargs))

    """
    Load methods by path
    """
    def load_mesh(self, path: str, *args, **kwargs) -> MeshGL:
        return self.register_drawable(self.factory.load_mesh(path, *args, **kwargs))

    def load_blocks(self, path: str, *args, **kwargs) -> BlockGL:
        return self.register_drawable(self.factory.load_blocks(path, *args, **kwargs))

    def load_points(self, path: str, *args, **kwargs) -> PointGL:
        return self.register_drawable(self.factory.load_points(path, *args, **kwargs))

    def load_lines(self, path: str, *args, **kwargs) -> LineGL:
        return self.register_drawable(self.factory.load_lines(path, *args, **kwargs))

    def load_tubes(self, path: str, *args, **kwargs) -> TubeGL:
        return self.register_drawable(self.factory.load_tubes(path, *args, **kwargs))

    def load_mesh_folder(self, path: str, *args, **kwargs) -> list:
        return self.load_folder(path, self.load_mesh, *args, **kwargs)

    def load_blocks_folder(self, path: str, *args, **kwargs) -> list:
        return self.load_folder(path, self.load_blocks, *args, **kwargs)

    def load_points_folder(self, path: str, *args, **kwargs) -> list:
        return self.load_folder(path, self.load_points, *args, **kwargs)

    def load_lines_folder(self, path: str, *args, **kwargs) -> list:
        return self.load_folder(path, self.load_lines, *args, **kwargs)

    def load_tubes_folder(self, path: str, *args, **kwargs) -> list:
        return self.load_folder(path, self.load_tubes, *args, **kwargs)

    """
    Generalized loaders
    """
    def load_folder(self, path: str, loader: callable, *args, **kwargs) -> list:
        return self.load_multiple(self.model.get_paths_from_directory(path), loader, *args, **kwargs)

    def load_multiple(self, path_list: list, loader: callable, *args, **kwargs) -> list:
        # Do not process if loading an empty path list
        if len(path_list) == 0:
            return []

        self.signal_process_started.emit()
        loaded = []

        for i, path in enumerate(path_list, 1):
            # Block only loaded signals
            self.blockSignals(True)
            drawable = loader(path, *args, **kwargs)
            self.blockSignals(False)

            if drawable is not None:
                loaded.append(drawable)

            self.signal_process_updated.emit(int(100 * i / len(path_list)))

        # Emit signals depending on results
        if len(loaded) > 0:
            self.signal_file_modified.emit()
            self.signal_load_success.emit(self.last_id)
        else:
            self.signal_load_failure.emit()

        self.signal_process_finished.emit()

        return loaded

    """
    Load methods by path (DEPRECATED)
    """
    @staticmethod
    def _deprecated_message(old: str, new: str, log: callable = warnings.warn) -> None:
        log(f'{old} is deprecated. Use {new} instead.', DeprecationWarning, 2)

    def mesh_by_path(self, path: str, *args, **kwargs) -> MeshGL:
        self._deprecated_message('mesh_by_path()', 'load_mesh()')
        return self.load_mesh(path, *args, **kwargs)

    def blocks_by_path(self, path: str, *args, **kwargs) -> BlockGL:
        self._deprecated_message('blocks_by_path()', 'load_blocks()')
        return self.load_blocks(path, *args, **kwargs)

    def points_by_path(self, path: str, *args, **kwargs) -> PointGL:
        self._deprecated_message('points_by_path()', 'load_points()')
        return self.load_points(path, *args, **kwargs)

    def lines_by_path(self, path: str, *args, **kwargs) -> LineGL:
        self._deprecated_message('lines_by_path()', 'load_lines()')
        return self.load_lines(path, *args, **kwargs)

    def tubes_by_path(self, path: str, *args, **kwargs) -> TubeGL:
        self._deprecated_message('tubes_by_path()', 'load_tubes()')
        return self.load_tubes(path, *args, **kwargs)

    def meshes_by_folder_path(self, path: str, *args, **kwargs) -> list:
        self._deprecated_message('meshes_by_folder_path()', 'load_mesh_folder()')
        return self.load_mesh_folder(path, *args, **kwargs)

    def blocks_by_folder_path(self, path: str, *args, **kwargs) -> list:
        self._deprecated_folder('blocks_by_folder_path()', 'load_blocks_folder()')
        return self.load_blocks_folder(path, *args, **kwargs)

    def points_by_folder_path(self, path: str, *args, **kwargs) -> list:
        self._deprecated_folder('points_by_folder_path()', 'load_points_folder()')
        return self.load_points_folder(path, *args, **kwargs)

    def lines_by_folder_path(self, path: str, *args, **kwargs) -> list:
        self._deprecated_folder('lines_by_folder_path()', 'load_lines_folder()')
        return self.load_lines_folder(path, *args, **kwargs)

    def tubes_by_folder_path(self, path: str, *args, **kwargs) -> list:
        self._deprecated_folder('tubes_by_folder_path()', 'load_tubes_folder()')
        return self.load_tubes_folder(path, *args, **kwargs)

    """
    Export methods
    """
    def _export_element(self, exporter: callable, path: str, _id: int) -> None:
        try:
            exporter(path, _id)
            self.signal_export_success.emit(_id)
        except Exception:
            self.signal_export_failure.emit()

    def export_mesh(self, path: str, _id: int) -> None:
        self._export_element(self.model.export_mesh, path, _id)

    def export_blocks(self, path: str, _id: int) -> None:
        self._export_element(self.model.export_blocks, path, _id)

    def export_points(self, path: str, _id: int) -> None:
        self._export_element(self.model.export_points, path, _id)

    def export_lines(self, path: str, _id: int) -> None:
        self._export_element(self.model.export_lines, path, _id)

    def export_tubes(self, path: str, _id: int) -> None:
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

    def plan_view(self) -> None:
        self.set_rotation_angle([0.0, 0.0, 0.0])

    def north_view(self) -> None:
        self.set_rotation_angle([270.0, 0.0, 270.0])

    def east_view(self) -> None:
        self.set_rotation_angle([270.0, 0.0, 0.0])

    def fit_to_bounds(self, min_bound: np.ndarray, max_bound: np.ndarray) -> None:
        center = (min_bound + max_bound) / 2
        self.rotation_center = center

        # Put the camera in a position that allow us to see between the boundaries.
        md = np.max(np.diff([min_bound, max_bound], axis=0))
        aspect = self.width() / self.height()
        fov_rad = self.fov * np.pi / 180.0

        # In perspective projection, we need a clever trigonometric calculation.
        if self.projection_mode == 'perspective':
            dist = (md / np.tan(fov_rad / 2) + md) / 2.0
            z_shift = dist * max(1.0, 1.0 / aspect)

        # But in orthographic projection, it's more direct.
        else:
            dist = md / 2
            z_shift = dist * max(1.0, aspect)

        camera_shift = center + np.array([0.0, 0.0, 1.1 * z_shift])
        self.set_camera_position(camera_shift)
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

        # Initialize collections
        self.background_collection.initialize()
        self.drawable_collection.initialize()
        self.axis_collection.initialize()

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

        # Update matrices
        self.drawable_collection.update_matrix('proj_matrix', self.proj)
        self.drawable_collection.update_matrix('model_view_matrix', self.camera * self.world)
        self.axis_collection.update_matrix('model_view_matrix', self.camera * self.world)

        # Draw every GLDrawable (meshes, blocks, points, etc)
        glEnable(GL_BLEND)
        self.background_collection.draw()
        self.drawable_collection.draw()
        self.axis_collection.draw()

        # Tick FPS counter
        self.fps_counter.tick()

    def resizeGL(self, w: float, h: float) -> None:
        aspect = w / h

        if self.projection_mode == 'perspective':
            self.proj.perspective(self.fov, aspect, 1.0, 100000.0)
        elif self.projection_mode == 'orthographic':
            z = self.off_center[2]
            self.proj.ortho(-z, z, -z / aspect, z / aspect, 0.0, 100000.0)

    """
    Utilities
    """
    def get_pixmap(self) -> QPixmap:
        pixmap = QPixmap(self.size())
        self.render(pixmap, QPoint(), QRegion(self.rect()))
        return pixmap

    def take_screenshot(self, save_path: str) -> None:
        if bool(save_path):
            self.get_pixmap().save(save_path)

    def screen_to_ndc(self, x: float, y: float, z: float) -> np.ndarray:
        # Click at bottom-left of screen => (-1.0, -1.0, z)
        # Click at top-right of screen => (1.0, 1.0, z)
        # But we can't really know where's z, so we just return 1.0
        return np.array([
            (2.0 * x / self.width()) - 1.0,
            1.0 - (2.0 * y / self.height()),
            1.0])

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

    def get_origin(self) -> np.ndarray:
        origin = (self.camera * self.world).inverted()[0].column(3).toVector3D()
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
            return self.get_origin()

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
        origin = self.get_origin()
        self.camera.translate(*offset)

        return origin

    def get_normal(self, origin_list, ray_list: list) -> np.ndarray:
        if self.projection_mode == 'perspective':
            # Perspective: Same origins, different rays
            normal = np.cross(*ray_list)
        else:
            # Orthographic: Same rays, different origins
            origin_diff = np.diff(origin_list, axis=0)[0]
            normal = np.cross(ray_list[0], origin_diff)

        return normal / np.linalg.norm(normal)

    @staticmethod
    def angles_from_vectors(normal: np.ndarray, up: np.ndarray) -> np.ndarray:
        # Returns a list of angles that allows the normal to look directly at the camera
        # Extrinsic: xyz / Intrinsic: XYZ (Tait-Bryan angles)
        # In self.paintGL, we're currently using the XYZ intrinsic rotation order.

        rotmat = QQuaternion.fromDirection(QVector3D(*normal), QVector3D(*up)).toRotationMatrix().data()
        return Rotation.from_matrix(np.array(rotmat).reshape((3, 3))).as_euler('XYZ', degrees=True)

    def set_camera_from_vectors(self, normal: np.ndarray, up: np.ndarray) -> None:
        # Auto-moves the camera using the normal as direction
        self.set_rotation_angle(self.angles_from_vectors(normal, up))

    def generate_slice_description(self, origin_list: list, ray_list: list) -> None:
        # A plane is created from `origin` and `ray_list`.
        # In perspective projection, the origin is the same.
        origin = origin_list[0]
        normal = self.get_normal(origin_list, ray_list)
        up = np.cross(ray_list[0], normal)
        up /= np.linalg.norm(up)

        # Emit description of the slice
        self.signal_slice_description.emit({
            'origin': origin,
            'normal': normal,
            'up': up,
        })

    def slice_meshes(self, origin: np.ndarray, normal: np.ndarray, include_hidden: bool = False) -> list:
        # By default, slice only visible meshes
        meshes = [m.element for m in self.drawable_collection.filter(MeshGL)
                  if m.is_visible or include_hidden]

        return self.model.slice_meshes(origin, normal, meshes)

    def slice_blocks(self, origin: np.ndarray, normal: np.ndarray, include_hidden: bool = True) -> list:
        # By default, slice visible and hidden blocks
        blocks = [m.element for m in self.drawable_collection.filter(BlockGL)
                  if m.is_visible or include_hidden]

        return self.model.slice_blocks(origin, normal, blocks)

    def measure_from_rays(self, origin_list: list, ray_list: list) -> None:
        meshes = [m.element for m in self.drawable_collection.filter(MeshGL) if m.is_visible]

        results = self.model.measure_from_rays(origin_list, ray_list, meshes)
        self.signal_mesh_distances.emit(results)

    def detect_mesh_intersection(self, x: float, y: float, z: float) -> None:
        ray = self.ray_from_click(x, y, z)
        origin = self.origin_from_click(x, y, z)
        meshes = [m.element for m in self.drawable_collection.filter(MeshGL) if m.is_visible]

        results = self.model.detect_mesh_intersection(ray, origin, meshes)
        self.signal_mesh_clicked.emit(results)

    """
    Controller
    """
    def add_controller(self, controller: Mode) -> None:
        self.controllers[controller.name] = controller

    def set_controller(self, mode_name: str) -> None:
        self.current_mode = self.controllers.get(mode_name)
        self.signal_mode_updated.emit(self.current_mode.name)
        self.update()

    def set_normal_mode(self) -> None:
        self.set_controller('Normal Mode')

    def set_detection_mode(self) -> None:
        self.set_controller('Detection Mode')

    def set_slice_mode(self) -> None:
        self.set_controller('Slice Mode')

    def set_measurement_mode(self) -> None:
        self.set_controller('Measurement Mode')

    """
    Events (dependent on current controller)
    """
    def mouseMoveEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseMoveEvent(event)
        self.update()

    def mousePressEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mousePressEvent(event)
        self.update()

    def mouseDoubleClickEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseDoubleClickEvent(event)
        self.update()

    def mouseReleaseEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseReleaseEvent(event)
        self.update()

    def wheelEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.wheelEvent(event)
        self.update()

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event, *args, **kwargs) -> None:
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if QFileInfo(path).isDir():
                self.load_folder(path, self.load_mesh)
            else:
                self.load_mesh(path)
